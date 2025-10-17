from langgraph.graph import StateGraph
from improving_states import ImprovingAgentGraphState, get_improving_agent_graph_state
from improving_agents import (
    PlannerAgent,
    SupervisorAgent,
    ProductOwnerAgent,
    RequirementEngineerAgent,
    QualityAssuranceAgent,
    RetrieveAgent,
    FinalUserStoryParserAgent,
)
import json
from langgraph.graph import StateGraph, END
from colorama import Fore, Style
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
import json


def supervisor_router(state):
    """Figure out which agent did the supervisor call to invoke it next"""
    supervisor_latest_response = get_improving_agent_graph_state(
        state, "supervisor_latest"
    ).content
    next_agent = json.loads(supervisor_latest_response)["next_agent"]
    if next_agent.lower() in {"end", "finish"}:
        return "final_story_parser"
    return next_agent


def to_retriever_router(state):
    """Figure out which agent called the RAG retriever, and get that agent's query for the retriever"""
    retriever_caller = get_improving_agent_graph_state(
        state, "agent_history_latest"
    ).content
    caller_message = get_improving_agent_graph_state(
        state, f"{retriever_caller}_latest"
    ).content
    message = json.loads(caller_message)
    return message["next_agent"]


def from_retriever_router(state):
    """Figure out which agent the RAG retriever should return its result to"""
    retriever_lastest_response = get_improving_agent_graph_state(
        state, "retriever_latest"
    ).content
    next_agent = json.loads(retriever_lastest_response)["next_agent"]
    return next_agent


def get_human_feedback(state):
    """Get human feedback"""
    feedback = input(
        Fore.GREEN
        + "> Human: please provide your feedback to the improved user story: "
        + Style.RESET_ALL
    )
    approval = input(
        Fore.GREEN
        + "> Human: does the improved user story pass your final approval (true/false)? "
        + Style.RESET_ALL
    )
    review = json.dumps(
        {
            "feedback": feedback,
            "final_approval": approval,
        }
    )
    state = {
        **state,
        "quality_assurance_response": add_messages(
            state["quality_assurance_response"], [HumanMessage(review)]
        ),
        "agent_history": add_messages(state["agent_history"], "quality_assurance"),
    }
    return state


def create_improving_graph(server=None, model=None, temperature=0):
    """Create the main graph"""
    graph = StateGraph(ImprovingAgentGraphState)

    # Adding nodes
    graph.add_node(
        "planner",
        lambda state: PlannerAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature,
        ).invoke(),
    )

    graph.add_node(
        "supervisor",
        lambda state: SupervisorAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature,
            agents=[
                "product_owner",
                "requirement_engineer",
                "quality_assurance",
                "end",
            ],
        ).invoke(
            agents=[
                "product_owner",
                "requirement_engineer",
                "quality_assurance",
                "end",
            ],
        ),
    )

    graph.add_node(
        "product_owner",
        lambda state: ProductOwnerAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature,
        ).invoke(),
    )

    graph.add_node(
        "requirement_engineer",
        lambda state: RequirementEngineerAgent(
            state=state,
            model=model,
            server=server,
            temperature=temperature,
        ).invoke(),
    )

    # graph.add_node(
    #     "quality_assurance",
    #     lambda state: QualityAssuranceAgent(
    #         state=state,
    #         model=model,
    #         server=server,
    #         temperature=temperature,
    #     ).invoke(),
    # )
    graph.add_node(
        "quality_assurance",
        get_human_feedback,
    )

    graph.add_node(
        "retriever",
        lambda state: RetrieveAgent(
            state=state, model=model, server=server, temperature=temperature
        ).invoke(),
    )

    graph.add_node(
        "final_story_parser",
        lambda state: FinalUserStoryParserAgent(state=state).invoke(),
    )

    # Adding edges
    graph.set_entry_point("planner")

    # Planner and QA will always report to supervisor
    for agent in [
        "planner",
        # "product_owner",
        # "requirement_engineer",
        "quality_assurance",
    ]:
        graph.add_edge(agent, "supervisor")

    # Adding conditional edges for retriever: PO and RE and call retriever, and retriver will return to them
    graph.add_conditional_edges("retriever", from_retriever_router)
    for agent in ["product_owner", "requirement_engineer"]:
        graph.add_conditional_edges(agent, to_retriever_router)

    # Supervisor will route to the next agent based on the response
    graph.add_conditional_edges("supervisor", supervisor_router)

    graph.add_edge("final_story_parser", END)

    return graph


def compile_workflow(graph):
    from langgraph.checkpoint.memory import MemorySaver

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
