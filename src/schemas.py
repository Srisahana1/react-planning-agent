from typing import Literal

from pydantic import BaseModel, Field


class AgentState(BaseModel):
    task: str
    observation: str = ""
    plan: str = ""
    action: str = ""
    action_input: str = ""
    result: str = ""
    reflection: str = ""
    final_answer: str = ""
    iteration: int = 0
    max_iterations: int = 3


class AgentDecision(BaseModel):
    action: Literal["calculate", "search_knowledge", "finish"] = Field(
        description="The next action the agent should take."
    )
    action_input: str = Field(
        description="Input to provide to the selected action."
    )
    reasoning: str = Field(
        description="Brief explanation for why this action was selected."
    )