from llms import get_open_ai, get_open_ai_json
from improving_states import ImprovingAgentGraphState, get_improving_agent_graph_state

from improving_prompts import (
    planner_system_prompt,
    planner_human_prompt,
    supervisor_human_prompt,
    supervisor_human_prompt_init,
    supervisor_system_prompt,
    product_owner_system_prompt,
    product_owner_human_prompt_init,
    product_owner_human_prompt,
    requirement_engineer_system_prompt,
    requirement_engineer_human_prompt_init,
    requirement_engineer_human_prompt,
    quality_assurance_human_prompt,
    quality_assurance_system_prompt,
)
import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages
from colorama import Fore, Back, Style
from langgraph.graph import StateGraph, END, START
from tools.tools import get_related_context

Color: dict = {"BOLD": "\033[1m", "NORMAL": "\033[0m"}


class ImprovingAgent:
    def __init__(
        self,
        state: ImprovingAgentGraphState,
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
        if get_improving_agent_graph_state(self.state, "retriever_latest") == []:
            return None
        retriever_message = get_improving_agent_graph_state(
            self.state, "retriever_latest"
        ).content
        retriever_message = json.loads(retriever_message)
        if retriever_message["next_agent"] == agent_name:
            return retriever_message["related_context"]
        else:
            return None


class PlannerAgent(ImprovingAgent):
    def invoke(self):
        user_story = get_improving_agent_graph_state(self.state, "original_user_story")
        human_prompt = planner_human_prompt.format(user_story=user_story)

        messages = [
            SystemMessage(planner_system_prompt),
            HumanMessage(human_prompt),
        ]

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        messages.append(AIMessage(response))

        self.update_state("planner_response", messages)
        self.update_state("agent_history", "planner")
        print(Fore.GREEN + f"> Planner: {response}")
        return self.state


class SupervisorAgent(ImprovingAgent):
    def __init__(
        self,
        state: ImprovingAgentGraphState,
        model=None,
        server=None,
        temperature=0,
        agents=[],
    ):
        super().__init__(state, model, server, temperature)
        system_prompt = supervisor_system_prompt.format(
            agents=agents,
        )
        messages = [SystemMessage(system_prompt)]

        self.update_state("supervisor_response", messages)

    def invoke(self, agents=[]):
        last_agent = get_improving_agent_graph_state(
            self.state, "agent_history_latest"
        ).content
        last_agent_message = get_improving_agent_graph_state(
            self.state, f"{last_agent}_latest"
        ).content

        messages = get_improving_agent_graph_state(self.state, "supervisor_all")
        # Decide whether to use to initial prompt or not
        if last_agent != "planner":
            messages.append(
                HumanMessage(
                    supervisor_human_prompt.format(
                        last_agent=last_agent,
                        last_agent_message=last_agent_message,
                        agents=agents,
                    )
                )
            )
        else:
            action_plan = get_improving_agent_graph_state(
                self.state, "planner_latest"
            ).content
            original_user_story = self.state["original_user_story"]
            messages.append(
                HumanMessage(
                    supervisor_human_prompt_init.format(
                        user_story=original_user_story, plan=action_plan, agents=agents
                    )
                )
            )

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content
        supervisor_response = json.loads(response)

        self.update_state("supervisor_response", [AIMessage(response)])
        self.update_state("agent_history", "supervisor")
        self.state["current_user_story"] = supervisor_response["improved_user_story"]
        print(
            Fore.CYAN
            + f"> Supervisor response:\n- Next agent: {supervisor_response['next_agent']}\n- Task: {supervisor_response['task']}\n- Improved user story:"
        )
        print(
            Color["BOLD"]
            + f"\n{supervisor_response['improved_user_story']}"
            + Color["NORMAL"]
        )
        return self.state


class RequirementEngineerAgent(ImprovingAgent):
    def __init__(
        self, state: ImprovingAgentGraphState, model=None, server=None, temperature=0
    ):
        super().__init__(state, model, server, temperature)
        messages = [SystemMessage(requirement_engineer_system_prompt)]
        self.update_state("requirement_engineer_response", messages)

    def invoke(self):
        supervisor_latest = get_improving_agent_graph_state(
            self.state, "supervisor_latest"
        ).content
        supervisor_task = json.loads(supervisor_latest)["task"]
        messages = get_improving_agent_graph_state(
            self.state, "requirement_engineer_all"
        )

        # Include the original user story if it's the first message
        if len(messages) == 1:
            original_user_story = self.state["original_user_story"]
            messages.append(
                HumanMessage(
                    requirement_engineer_human_prompt_init.format(
                        user_story=original_user_story, task=supervisor_task
                    )
                )
            )
        else:
            related_content = self.get_retrieved_content("requirement_engineer")
            current_user_story = self.state["current_user_story"]
            messages.append(
                HumanMessage(
                    requirement_engineer_human_prompt.format(
                        task=supervisor_task, improved_user_story=current_user_story
                    )
                    if related_content is None
                    else requirement_engineer_human_prompt.format(
                        task=supervisor_task, improved_user_story=current_user_story
                    )
                    + f"\nRelated context for the task: \n{related_content}"
                )
            )

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("requirement_engineer_response", [AIMessage(response)])
        self.update_state("agent_history", "requirement_engineer")
        print(Fore.YELLOW + f"> Requirement Engineer: {response}")
        return self.state


class ProductOwnerAgent(ImprovingAgent):
    def __init__(
        self, state: ImprovingAgentGraphState, model=None, server=None, temperature=0
    ):
        super().__init__(state, model, server, temperature)
        messages = [SystemMessage(product_owner_system_prompt)]
        self.update_state("product_owner_response", messages)

    def invoke(self):
        supervisor_latest = get_improving_agent_graph_state(
            self.state, "supervisor_latest"
        ).content
        supervisor_task = json.loads(supervisor_latest)["task"]
        messages = get_improving_agent_graph_state(self.state, "product_owner_all")

        if len(messages) == 1:
            original_user_story = self.state["original_user_story"]
            messages.append(
                HumanMessage(
                    product_owner_human_prompt_init.format(
                        user_story=original_user_story, task=supervisor_task
                    )
                )
            )
        else:
            related_content = self.get_retrieved_content("product_owner")
            current_user_story = self.state["current_user_story"]
            messages.append(
                HumanMessage(
                    requirement_engineer_human_prompt.format(
                        task=supervisor_task, improved_user_story=current_user_story
                    )
                    if related_content is None
                    else requirement_engineer_human_prompt.format(
                        task=supervisor_task, improved_user_story=current_user_story
                    )
                    + f"\nRelated context for the task: \n{related_content}"
                )
            )

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("product_owner_response", [AIMessage(response)])
        self.update_state("agent_history", "product_owner")
        print(Fore.MAGENTA + f"> Product Owner: {response}")
        return self.state


class QualityAssuranceAgent(ImprovingAgent):
    def __init__(
        self, state: ImprovingAgentGraphState, model=None, server=None, temperature=0
    ):
        super().__init__(state, model, server, temperature)
        messages = [SystemMessage(quality_assurance_system_prompt)]
        self.update_state("quality_assurance_response", messages)

    def invoke(self):
        supervisor_latest = get_improving_agent_graph_state(
            self.state, "supervisor_latest"
        ).content
        improved_user_story = json.loads(supervisor_latest)["improved_user_story"]
        messages = get_improving_agent_graph_state(self.state, "quality_assurance_all")
        messages.append(
            HumanMessage(
                quality_assurance_human_prompt.format(user_story=improved_user_story)
            )
        )

        llm = self.get_llm()
        ai_msg = llm.invoke(messages)
        response = ai_msg.content

        self.update_state("quality_assurance_response", [AIMessage(response)])
        self.update_state("agent_history", "quality_assurance")
        print(Fore.BLUE + f"> Quality Assurance: {response}")
        return self.state


class RetrieveAgent(ImprovingAgent):
    def invoke(self):
        last_agent = get_improving_agent_graph_state(
            self.state, "agent_history_latest"
        ).content
        last_agent_message = get_improving_agent_graph_state(
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
                + f"> Retriever: Found some related context for the query:\n{query}\nPassing the context to {last_agent}..."
            )
            # print(f"> Related context: {related_context}")
        else:
            self.update_state(
                "retriever_response",
                [
                    AIMessage(
                        json.dumps({"next_agent": last_agent, "related_context": None})
                    )
                ],
            )
            print(Fore.LIGHTBLUE_EX + "> Retriever: No query provided!")

        return self.state


class FinalUserStoryParserAgent(ImprovingAgent):
    """This agent parse the final user story from the Supervisor into the state"""

    def invoke(self):
        all_user_stories = get_improving_agent_graph_state(
            self.state, "user_stories_all"
        )
        supervisor_latest = get_improving_agent_graph_state(
            self.state, "supervisor_latest"
        ).content
        supervisor_response = json.loads(supervisor_latest)
        story_id = len(all_user_stories) + 1
        final_story = supervisor_response["improved_user_story"]
        self.update_state(
            "user_stories_history",
            HumanMessage(
                json.dumps({"id": f"US{story_id}", "user_story": final_story})
            ),
        )
        print(
            Fore.RED
            + f"> Final user story parser: US number {story_id}:\n{final_story}"
        )
        return self.state
