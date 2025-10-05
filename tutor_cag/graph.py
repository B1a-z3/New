from typing import Callable, Dict, List, Optional, Any
from pydantic import BaseModel, ConfigDict
import networkx as nx

class Message(BaseModel):
    role: str
    content: str
    meta: dict = {}

class Agent(BaseModel):
    name: str
    description: str
    handle: Callable[[List[Message]], Message]
    # Allow callable fields without pydantic trying to generate schema
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Router(BaseModel):
    name: str
    description: str
    route: Callable[[List[Message]], str]
    model_config = ConfigDict(arbitrary_types_allowed=True)

class CAG(BaseModel):
    graph: nx.DiGraph
    entrypoint: str
    # Allow networkx graph type
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def run(self, history: List[Message]) -> Message:
        current = self.entrypoint
        while True:
            node = self.graph.nodes[current]
            if node.get("type") == "agent":
                agent: Agent = node["impl"]
                response = agent.handle(history)
                history.append(response)
                # decide next via default edge or stop
                successors = list(self.graph.successors(current))
                if not successors:
                    return response
                current = successors[0]
            elif node.get("type") == "router":
                router: Router = node["impl"]
                next_node = router.route(history)
                if next_node not in self.graph[current]:
                    # fallback to default if invalid
                    successors = list(self.graph.successors(current))
                    current = successors[0] if successors else current
                else:
                    current = next_node
            else:
                return Message(role="system", content="Reached terminal node.")


def run_tutor_session(graph: CAG, user_input: str) -> str:
    history: List[Message] = [Message(role="user", content=user_input)]
    final = graph.run(history)
    return final.content
