# ADR-0001: Hand-rolled agent loop before LangGraph

- **Status:** Accepted (recommendation)
- **Date:** 2026-06-03

> This blueprint records architectural decisions as **recommendations** for real
> projects you'll build on its shape. The repo itself contains no code, so the
> decision applies the first time you implement `agent/graph.py`.

## Context

An agent needs a plan → act → observe control loop with bounded iteration and a
clear place to gate tool calls. LangGraph is the obvious production choice. But
LangGraph pulls in `langchain-core` and a non-trivial dependency tree, and its
graph/state API is a learning curve that obscures *what the agent actually does*.

For a first version - and especially for a portfolio or teaching artifact - a
tiny hand-rolled loop is easier to read, test, and explain.

## Decision

Ship a small, dependency-free orchestrator (`agent/graph.py` + `agent/nodes.py`)
that implements the bounded plan/act/observe loop directly. Keep `langgraph` as
an optional extra in `pyproject.toml`. Keep the public surface (`Agent.ainvoke`)
stable so porting to a compiled `StateGraph` later is a localized change.

## Consequences

- The loop can be ~40 lines and fully readable; tests don't need a graph runtime.
- You own concerns LangGraph would provide (checkpointing, streaming, retries,
  parallel branches). When you need them, port - new ADR.
- Node functions should take `(deps, state)` so they map cleanly onto LangGraph
  nodes; the migration cost is contained.

## Alternatives considered

- **Adopt LangGraph from day one** - best long term, heavier deps, steeper read.
  Deferred, not rejected.
- **A generic agent framework (CrewAI, AutoGen, ...)** - more opinionated and
  heavier than the problem; would bury the architecture.
