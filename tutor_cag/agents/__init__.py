from typing import List
from ..graph import Message, Agent
from ..kb.snippets import search_snippets


def make_math_stats_agent() -> Agent:
    def handle(history: List[Message]) -> Message:
        last = next((m for m in reversed(history) if m.role == "user"), None)
        query = last.content if last else ""
        docs = search_snippets(query, domains=["math", "stats"])
        bullet_lines = [f"- {d['title']}: {d['summary']}" for d in docs[:5]]
        content = "\n".join(["Here's a helpful explanation with references:", "", *bullet_lines])
        return Message(role="assistant", content=content)

    return Agent(name="math_stats_tutor", description="Explains math & statistics", handle=handle)


def make_ml_agent() -> Agent:
    def handle(history: List[Message]) -> Message:
        last = next((m for m in reversed(history) if m.role == "user"), None)
        query = last.content if last else ""
        docs = search_snippets(query, domains=["ml"])
        bullet_lines = [f"- {d['title']}: {d['summary']}" for d in docs[:5]]
        content = "\n".join(["Let's break this down:", "", *bullet_lines])
        return Message(role="assistant", content=content)

    return Agent(name="ml_tutor", description="Explains ML concepts", handle=handle)


