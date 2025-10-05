from tutor_cag.cli import build_graph
from tutor_cag.graph import Message


def test_smoke():
    graph = build_graph()
    resp = graph.run([Message(role="user", content="Explain bias variance tradeoff")])
    assert "Bias-Variance" in resp.content
