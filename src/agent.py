from langchain_ollama import ChatOllama

from src.schemas import AgentDecision
from src.tools import calculate, search_knowledge


MODEL_NAME = "llama3.2"

llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)


def decide_next_action(
    task: str,
    observation: str = "",
    iteration: int = 0,
) -> AgentDecision:
    prompt = f"""
You are a ReAct planning agent.

Available actions:

1. calculate
   Use this for mathematical calculations.
   action_input MUST contain the mathematical expression.
   Example:
   Task: Calculate 25 * 8
   action: calculate
   action_input: 25 * 8

2. search_knowledge
   Use this for questions about RAG, ReAct, or LangGraph.
   action_input MUST contain the topic or question being searched.
   Example:
   Task: What is ReAct?
   action: search_knowledge
   action_input: ReAct

3. finish
   Use this when the previous observation contains enough information
   to answer the user's task.
   action_input MUST contain the final answer.

User task:
{task}

Previous observation:
{observation}

Current iteration:
{iteration}

RULES:
- Never return an empty action_input.
- If there is no previous observation, select the appropriate tool.
- If the previous observation already answers the task, select finish.
- Never repeat a tool when its result is already in previous observation.
- When selecting finish, place the final response in action_input.
- Keep reasoning brief.

Choose exactly one action.
"""

    structured_llm = llm.with_structured_output(AgentDecision)
    return structured_llm.invoke(prompt)


def execute_action(decision: AgentDecision) -> str:
    if decision.action == "calculate":
        return calculate(decision.action_input)

    if decision.action == "search_knowledge":
        return search_knowledge(decision.action_input)

    if decision.action == "finish":
        return decision.action_input

    return "Unknown action."