from unittest.mock import patch

from src.schemas import AgentDecision
from src.workflow import run_agent


@patch("src.workflow.decide_next_action")
def test_knowledge_agent(mock_decision):
    mock_decision.return_value = AgentDecision(
        action="search_knowledge",
        action_input="ReAct",
        reasoning="Search the local knowledge base.",
    )

    result = run_agent("What is ReAct?")

    assert result.action == "finish"
    assert "ReAct" in result.final_answer
    assert result.iteration == 2


@patch("src.workflow.decide_next_action")
def test_calculator_agent(mock_decision):
    mock_decision.return_value = AgentDecision(
        action="calculate",
        action_input="25 * 8",
        reasoning="Calculate the expression.",
    )

    result = run_agent("Calculate 25 * 8")

    assert result.action == "finish"
    assert result.final_answer == "200"
    assert result.iteration == 2