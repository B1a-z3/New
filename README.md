# Tutor-CAG

Data science tutor chatbot using a simple Composable Agent Graph (CAG). It routes questions between a math/statistics tutor and a machine learning tutor and replies with concise, referenced summaries.

## Install

Requirements: Python 3.10+

```bash
python3 -m pip install -e .
```

If you cannot create a venv in this environment, install system-wide as above.

## CLI Usage

```bash
python -m tutor_cag.cli chat "Explain the bias-variance tradeoff"
# or after install
tutor-cag chat "What is cross validation?"
```

## How it works (CAG)

- Router node `topic_router` inspects the latest user message and picks either `math` or `ml` agent.
- Agents look up a tiny in-repo knowledge base and compose an answer with bullet references.

Key files:

- `tutor_cag/graph.py`: minimal CAG runtime with `Message`, `Agent`, `Router`, and `CAG`.
- `tutor_cag/cli.py`: builds the graph and exposes the CLI.
- `tutor_cag/agents/__init__.py`: domain agents for math/stats and ML.
- `tutor_cag/kb/snippets.py`: small knowledge base.
- `tests/test_smoke.py`: smoke test for routing and answer content.

## Test

```bash
python -m pytest -q
```
