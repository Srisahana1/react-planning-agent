from fastapi import FastAPI
from pydantic import BaseModel

from src.schemas import AgentState
from src.workflow import run_agent


app = FastAPI(
    title="ReAct Planning Agent",
    description=(
        "A ReAct-style AI agent that reasons, selects tools, "
        "executes actions, observes results, and determines when to finish."
    ),
    version="1.0.0",
)


class AgentRequest(BaseModel):
    task: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/run", response_model=AgentState)
def run(request: AgentRequest):
    return run_agent(request.task)