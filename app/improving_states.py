from typing import TypedDict, Annotated, Sequence
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


# Define the state object for the agent graph
class ImprovingAgentGraphState(TypedDict):
    original_user_story: str
    current_user_story: str
    # Storing all the improved user stories that the system has generated
    user_stories_history: Annotated[Sequence[BaseMessage], add_messages]
    planner_response: Annotated[Sequence[BaseMessage], add_messages]
    supervisor_response: Annotated[Sequence[BaseMessage], add_messages]
    requirement_engineer_response: Annotated[Sequence[BaseMessage], add_messages]
    product_owner_response: Annotated[Sequence[BaseMessage], add_messages]
    quality_assurance_response: Annotated[Sequence[BaseMessage], add_messages]
    retriever_response: Annotated[Sequence[BaseMessage], add_messages]
    # Kinda like a conversation history, where we store the agent name in order
    agent_history: Annotated[list, add_messages]


# Define the nodes in the agent graph
def get_improving_agent_graph_state(state: ImprovingAgentGraphState, state_key: str):
    state_mapping = {
        "planner_all": state["planner_response"],
        "planner_latest": (
            state["planner_response"][-1]
            if state["planner_response"]
            else state["planner_response"]
        ),
        "supervisor_all": state["supervisor_response"],
        "supervisor_latest": (
            state["supervisor_response"][-1]
            if state["supervisor_response"]
            else state["supervisor_response"]
        ),
        "requirement_engineer_all": state["requirement_engineer_response"],
        "requirement_engineer_latest": (
            state["requirement_engineer_response"][-1]
            if state["requirement_engineer_response"]
            else state["requirement_engineer_response"]
        ),
        "product_owner_all": state["product_owner_response"],
        "product_owner_latest": (
            state["product_owner_response"][-1]
            if state["product_owner_response"]
            else state["product_owner_response"]
        ),
        "quality_assurance_all": state["quality_assurance_response"],
        "quality_assurance_latest": (
            state["quality_assurance_response"][-1]
            if state["quality_assurance_response"]
            else state["quality_assurance_response"]
        ),
        "retriever_all": state["retriever_response"],
        "retriever_latest": (
            state["retriever_response"][-1]
            if state["retriever_response"]
            else state["retriever_response"]
        ),
        "agent_history_all": state["agent_history"],
        "agent_history_latest": (
            state["agent_history"][-1]
            if state["agent_history"]
            else state["agent_history"]
        ),
        "user_stories_all": state["user_stories_history"],
    }
    return state_mapping.get(state_key, None)


state = {
    "original_user_story": "",
    "current_user_story": "",
    "user_stories_history": [],
    "planner_response": [],
    "supervisor_response": [],
    "requirement_engineer_response": [],
    "product_owner_response": [],
    "quality_assurance_response": [],
    "agent_history": [],
}
#
