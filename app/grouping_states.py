from typing import TypedDict, Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


# Define the state object for the agent graph
class GroupingAgentGraphState(TypedDict):
    user_stories: Annotated[Sequence[BaseMessage], add_messages]
    grouper_response: Annotated[Sequence[BaseMessage], add_messages]
    retriever_response: Annotated[Sequence[BaseMessage], add_messages]
    quality_assurance_response: Annotated[Sequence[BaseMessage], add_messages]
    grouped_stories: list[str]
    jira_linked_stories: list[str]
    # Stuff for Jira ticket linking
    jira_retriever_response: Annotated[Sequence[BaseMessage], add_messages]
    jira_linker_response: Annotated[Sequence[BaseMessage], add_messages]
    # Kinda like a conversation history, where we store the agent name in order
    agent_history: Annotated[list, add_messages]


# Define the nodes in the agent graph
def get_grouping_agent_graph_state(state: GroupingAgentGraphState, state_key: str):
    state_mapping = {
        "grouper_all": state["grouper_response"],
        "grouper_latest": (
            state["grouper_response"][-1]
            if state["grouper_response"]
            else state["grouper_response"]
        ),
        "retriever_all": state["retriever_response"],
        "retriever_latest": (
            state["retriever_response"][-1]
            if state["retriever_response"]
            else state["retriever_response"]
        ),
        "quality_assurance_all": state["quality_assurance_response"],
        "quality_assurance_latest": (
            state["quality_assurance_response"][-1]
            if state["quality_assurance_response"]
            else state["quality_assurance_response"]
        ),
        "jira_linker_all": state["jira_linker_response"],
        "jira_linker_latest": (
            state["jira_linker_response"][-1]
            if state["jira_linker_response"]
            else state["jira_linker_response"]
        ),
        "jira_retriever_all": state["jira_retriever_response"],
        "jira_retriever_latest": (
            state["jira_retriever_response"][-1]
            if state["jira_retriever_response"]
            else state["jira_retriever_response"]
        ),
        "user_stories_all": state["user_stories"],
        "agent_history_all": state["agent_history"],
        "agent_history_latest": (
            state["agent_history"][-1]
            if state["agent_history"]
            else state["agent_history"]
        ),
    }
    return state_mapping.get(state_key, None)


state = {
    "user_stories": [],
    "grouper_response": [],
    "retriever_response": [],
    "quality_assurance_response": [],
    "jira_linker_response": [],
    "jira_retriever_response": [],
    "grouped_stories": [],
    "jira_linked_stories": [],
    "agent_history": [],
}
