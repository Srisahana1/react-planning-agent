from langgraph.graph import END, StateGraph

from src.agent import decide_next_action, execute_action
from src.schemas import AgentState


def agent_step(state: AgentState) -> AgentState:
    # If we already have a successful tool observation,
    # finish instead of calling the same tool repeatedly.
    if state.observation and not state.observation.startswith(
        ("No relevant information", "Calculation error")
    ):
        state.action = "finish"
        state.action_input = state.observation
        state.result = state.observation
        state.reflection = "The previous observation contains enough information."
        state.final_answer = state.observation
        state.iteration += 1
        return state

    decision = decide_next_action(
        task=state.task,
        observation=state.observation,
        iteration=state.iteration,
    )

    result = execute_action(decision)

    state.action = decision.action
    state.action_input = decision.action_input
    state.result = result
    state.reflection = decision.reasoning
    state.iteration += 1

    if decision.action == "finish":
        state.final_answer = result
    else:
        state.observation = result

    return state


def should_continue(state: AgentState) -> str:
    if state.action == "finish":
        return "end"

    if state.iteration >= state.max_iterations:
        state.final_answer = state.observation
        return "end"

    return "continue"


workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_step)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "agent",
        "end": END,
    },
)

react_agent = workflow.compile()


def run_agent(task: str) -> AgentState:
    initial_state = AgentState(task=task)

    result = react_agent.invoke(initial_state)

    return AgentState.model_validate(result)