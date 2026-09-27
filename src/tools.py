import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right),
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](_evaluate(node.operand))

    raise ValueError("Unsupported expression")


def calculate(expression: str) -> str:
    """Safely evaluate a basic mathematical expression."""
    try:
        tree = ast.parse(expression, mode="eval")
        return str(_evaluate(tree.body))
    except Exception as exc:
        return f"Calculation error: {exc}"


def search_knowledge(query: str) -> str:
    """Return information from a small local knowledge base."""
    knowledge = {
        "rag": (
            "RAG combines information retrieval with language-model "
            "generation so answers can use retrieved context."
        ),
        "react": (
            "ReAct is an agent pattern that combines reasoning and actions "
            "in an iterative workflow."
        ),
        "langgraph": (
            "LangGraph is a framework for building stateful workflows "
            "and agent systems using graphs."
        ),
    }

    query_lower = query.lower()

    for key, value in knowledge.items():
        if key in query_lower:
            return value

    return "No relevant information was found in the local knowledge base."