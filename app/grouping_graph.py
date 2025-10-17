from langgraph.graph import StateGraph
from grouping_states import GroupingAgentGraphState, get_grouping_agent_graph_state
from grouping_agents import (
    RetrieveAgent,
    GrouperAgent,
    GroupedStoriesParserAgent,
    JiraTicketLinkerAgent,
    JiraRetrieverAgent,
)
import json
from langgraph.graph import StateGraph, END
from colorama import Fore, Style
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
import json


def grouper_router(state):
    """Figure out which agent did the grouper call to invoke it next"""
    grouper_latest_response = get_grouping_agent_graph_state(
        state, "grouper_latest"
    ).content
    next_agent = json.loads(grouper_latest_response)["next_agent"]
    print(f"> Next agent: {next_agent}")
    if next_agent.lower() in {"end", "finish"}:
        return "jira_retriever"
    return next_agent


def linker_router(state):
    linker_latest_response = get_grouping_agent_graph_state(
        state, "jira_linker_latest"
    ).content
    next_agent = json.loads(linker_latest_response)["next_agent"]
    print(f"> Next agent: {next_agent}")
    if next_agent.lower() in {"end", "finish"}:
        return "final_parser"
    return next_agent


def retriever_router(state):
    retriever_lastest_response = get_grouping_agent_graph_state(
        state, "retriever_latest"
    ).content
    next_agent = json.loads(retriever_lastest_response)["next_agent"]
    return next_agent


def quality_assurance_router(state):
    qa_latest_response = get_grouping_agent_graph_state(
        state, "quality_assurance_latest"
    ).content
    next_agent = json.loads(qa_latest_response)["next_agent"]
    return next_agent


def get_human_feedback(state):
    last_agent = get_grouping_agent_graph_state(state, "agent_history_latest").content
    feedback = input(
        Fore.GREEN
        + "> Human: please provide your feedback to the results: "
        + Style.RESET_ALL
    )
    approval = input(
        Fore.GREEN
        + "> Human: do the results pass your final approval (true/false)? "
        + Style.RESET_ALL
    )
    review = json.dumps(
        {
            "feedback": feedback,
            "final_approval": approval,
            "next_agent": last_agent,
        }
    )
    state = {
        **state,
        "quality_assurance_response": add_messages(
            state["quality_assurance_response"], [HumanMessage(review)]
        ),
    }
    return state


def create_grouping_graph(server=None, model=None, temperature=0):
    """Create the main graph"""
    graph = StateGraph(GroupingAgentGraphState)

    # Adding nodes
    graph.add_node(
        "grouper",
        lambda state: GrouperAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature,
            agents=["quality_assurance", "FINISH", "retriever"],
        ).invoke(),
    )

    graph.add_node(
        "jira_retriever",
        lambda state: JiraRetrieverAgent(
            state=state, model=model, server=server, temperature=temperature
        ).invoke(),
    )

    graph.add_node(
        "jira_linker",
        lambda state: JiraTicketLinkerAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature,
            agents=["quality_assurance", "FINISH", "retriever"],
        ).invoke(),
    )

    graph.add_node(
        "quality_assurance",
        get_human_feedback,
    )

    graph.add_node(
        "final_parser",
        lambda state: GroupedStoriesParserAgent(
            state=state, model=model, server=server, temperature=temperature
        ).invoke(),
    )

    graph.add_node(
        "retriever",
        lambda state: RetrieveAgent(
            state=state, model=model, server=server, temperature=temperature
        ).invoke(),
    )

    # Adding edges
    graph.set_entry_point("grouper")

    graph.add_conditional_edges("grouper", grouper_router)

    graph.add_edge("jira_retriever", "jira_linker")

    graph.add_conditional_edges("jira_linker", linker_router)
    graph.add_conditional_edges("retriever", retriever_router)
    graph.add_conditional_edges("quality_assurance", quality_assurance_router)

    graph.add_edge("final_parser", END)

    return graph
