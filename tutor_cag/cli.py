from typing import List
import typer
from rich.console import Console
from rich.panel import Panel
from .graph import CAG, Message, Router
from .agents import make_math_stats_agent, make_ml_agent
import networkx as nx

console = Console()
app = typer.Typer(add_completion=False)


def build_graph() -> CAG:
    g = nx.DiGraph()

    math_agent = make_math_stats_agent()
    ml_agent = make_ml_agent()

    def router_route(history: List[Message]) -> str:
        last_user = next((m for m in reversed(history) if m.role == "user"), None)
        text = (last_user.content if last_user else "").lower()
        # Strong signal for ML when both 'bias' and 'variance' appear
        if "bias" in text and "variance" in text:
            return "ml"
        ml_keywords = [
            "regression",
            "classification",
            "model",
            "gradient",
            "overfitting",
            "underfitting",
            "cross validation",
            "cross-validation",
            "training",
            "train ",
            "test set",
            "optimizer",
            "gradient descent",
            "tradeoff",
        ]
        if any(k in text for k in ml_keywords):
            return "ml"
        return "math"

    router = Router(name="topic_router", description="Routes to math/stats or ML", route=router_route)

    g.add_node("router", type="router", impl=router)
    g.add_node("math", type="agent", impl=math_agent)
    g.add_node("ml", type="agent", impl=ml_agent)

    g.add_edge("router", "math")
    g.add_edge("router", "ml")

    return CAG(graph=g, entrypoint="router")


@app.command()
def chat(question: List[str] = typer.Argument(..., help="Your question")):
    graph = build_graph()
    user_input = " ".join(question)
    response = graph.run([Message(role="user", content=user_input)])
    console.print(Panel.fit(response.content, title="Tutor"))


if __name__ == "__main__":
    app()
