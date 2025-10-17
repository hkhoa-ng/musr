from llms import get_open_ai, get_open_ai_json
from grouping_states import GroupingAgentGraphState, get_grouping_agent_graph_state
from grouping_prompts import (
    grouper_system_prompt,
    grouper_human_prompt,
    grouper_human_prompt_init,
    linker_human_prompt,
    linker_human_prompt_init,
    linker_system_prompt,
)
import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from colorama import Fore, Back, Style
from langgraph.graph import StateGraph, END, START
from tools.tools import get_related_context
from tools.mock_jira import get_jira_tickets

Color: dict = {"BOLD": "\033[1m", "NORMAL": "\033[0m"}


class GroupingAgent:
    def __init__(
        self,
        state: GroupingAgentGraphState,
        model=None,
        server=None,
        temperature=0,
    ):
        self.state = state
        self.model = model
        self.server = server
        self.temperature = temperature

    def get_llm(self, json_model=True):
        if self.server == "openai":
            return (
                get_open_ai_json(model=self.model, temperature=self.temperature)
                if json_model
                else get_open_ai(model=self.model, temperature=self.temperature)
            )

    def update_state(self, key, value):
        self.state = {
            **self.state,
            key: add_messages(self.state[key], value),
        }

    def get_retrieved_content(self, agent_name: str):
        if get_grouping_agent_graph_state(self.state, "retriever_latest") == []:
            return None
        retriever_message = get_grouping_agent_graph_state(
            self.state, "retriever_latest"
        ).content
        retriever_message = json.loads(retriever_message)
        if retriever_message["next_agent"] == agent_name:
            return retriever_message["related_context"]
        else:
            return None


class RetrieveAgent(GroupingAgent):
    def invoke(self):
        last_agent = get_grouping_agent_graph_state(
            self.state, "agent_history_latest"
        ).content
        last_agent_message = get_grouping_agent_graph_state(
            self.state, f"{last_agent}_latest"
        ).content
        query = json.loads(last_agent_message)["query"]
        if query:
            related_context = get_related_context(query)
            self.update_state(
                "retriever_response",
                [
                    AIMessage(
                        json.dumps(
                            {
                                "next_agent": last_agent,
                                "related_context": related_context,
                            }
                        )
                    )
                ],
            )
            self.update_state("agent_history", "retriever")
            print(
                Fore.LIGHTBLUE_EX
                + f"> Retriever: Found some related context for the query:\n{query}\nPassing the context to caller..."
            )
        else:
            self.update_state(
                "retriever_response",
                [AIMessage(None)],
            )
            self.update_state("agent_history", "retriever")
            print(Fore.LIGHTBLUE_EX + "> Retriever: No query provided!")

        return self.state


class JiraRetrieverAgent(GroupingAgent):
    def invoke(self):
        # TODO: Implement actual Jira API call here later...

        tickets = get_jira_tickets()

        print(Fore.LIGHTBLUE_EX + f"> Jira Retriever: Got some Jira tickets!")

        self.update_state("jira_retriever_response", [AIMessage(json.dumps(tickets))])
        return self.state


class GrouperAgent(GroupingAgent):
    def __init__(
        self,
        state: GroupingAgentGraphState,
        model=None,
        server=None,
        temperature=0,
        agents=[],
    ):
        super().__init__(state, model, server, temperature)
        system_prompt = grouper_system_prompt.format(
            agents=(agents),
        )
        messages = [SystemMessage(system_prompt)]
        self.update_state("grouper_response", messages)

    def invoke(self):
        messages = get_grouping_agent_graph_state(self.state, "grouper_all")

        # Include the user stories & Jira ticket if it's the first message
        if len(messages) == 1:
            user_stories = self.state["user_stories"]
            messages.append(
                HumanMessage(
                    grouper_human_prompt_init.format(user_stories=user_stories)
                )
            )
        # If not the first message, include the related context and feedback (if available)
        else:
            related_content = self.get_retrieved_content("grouper")
            feedback = get_grouping_agent_graph_state(
                self.state, "quality_assurance_latest"
            )

            # Constructing the prompt with related content, feedback, and user stories
            prompt = grouper_human_prompt.format(
                related_content=related_content if related_content is not None else "",
                feedback=feedback.content if type(feedback) is HumanMessage else "",
            )

            messages.append(HumanMessage(prompt))

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("grouper_response", [AIMessage(response)])
        self.update_state("agent_history", "grouper")
        print(Fore.YELLOW + f"> User Story Grouper: {response}")

        return self.state


class JiraTicketLinkerAgent(GroupingAgent):
    def __init__(
        self,
        state: GroupingAgentGraphState,
        model=None,
        server=None,
        temperature=0,
        agents=[],
    ):
        super().__init__(state, model, server, temperature)
        system_prompt = linker_system_prompt.format(
            agents=(agents),
        )
        messages = [SystemMessage(system_prompt)]
        self.update_state("jira_linker_response", messages)

    def invoke(self):
        messages = get_grouping_agent_graph_state(self.state, "jira_linker_all")

        # Include the user stories to link and the Jira tickets if it's the first message
        if len(messages) == 1:
            user_stories = self.state["user_stories"]
            tickets = get_grouping_agent_graph_state(
                self.state, "jira_retriever_latest"
            )
            messages.append(
                HumanMessage(
                    linker_human_prompt_init.format(
                        user_stories=user_stories, jira_tickets=tickets.content
                    )
                )
            )
        else:
            related_content = self.get_retrieved_content("jira_linker")
            feedback = get_grouping_agent_graph_state(
                self.state, "quality_assurance_latest"
            )

            # Constructing the prompt with related content, feedback, and user stories
            prompt = linker_human_prompt.format(
                related_content=related_content if related_content is not None else "",
                feedback=feedback.content if feedback.content is not None else "",
            )

            messages.append(HumanMessage(prompt))

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("jira_linker_response", [AIMessage(response)])
        self.update_state("agent_history", "jira_linker")
        print(Fore.CYAN + f"> Jira Ticket Linker: {response}")

        linked_stories = json.loads(response)["linked_stories"]
        self.state["jira_linked_stories"] = linked_stories

        return self.state


class GroupedStoriesParserAgent(GroupingAgent):
    def invoke(self):
        grouper_latest = get_grouping_agent_graph_state(
            self.state, "grouper_latest"
        ).content
        grouper_response = json.loads(grouper_latest)
        grouped_stories = grouper_response["grouped_stories"]
        self.state["grouped_stories"] = grouped_stories
        print(Fore.RED + f"> Final Grouped Stories:")
        for group in grouped_stories:

            print("_____")
            print(f"| Group: {group['group_name']}")
            print(f"| Stories in group: {group['user_stories']}")
            print(f"| Common theme: {group['feature']}")
            print(f"| Details: {group['details']}")
            print("_____")
        return self.state
