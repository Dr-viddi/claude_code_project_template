# ADR-0001: Hand-rolled agent loop instead of LangGraph (for now)

- **Status:** Accepted
- **Date:** 2026-06-03

## Context

The agent needs a plan → act → observe control loop with bounded iteration and a
clear place to gate tool calls. LangGraph is the obvious production choice and the
target this repo is structured for (`agent/graph.py` mirrors a `StateGraph`). But
LangGraph pulls in `langchain-core` and a non-trivial dependency tree, and its
graph/state API is a learning curve that obscures *what the agent actually does*.

A core goal of this repo is that it runs on a fresh clone with no API key, no
services, and a dependency set small enough to read in one sitting - both for fast
onboarding and so a reviewer can understand the whole loop quickly.

## Decision

Ship a small, dependency-free orchestrator (`agent/graph.py` + `agent/nodes.py`)
that implements the bounded plan/act/observe loop directly. Keep `langgraph` as an
optional extra and keep the public surface (`Agent.ainvoke`) stable so porting to a
compiled `StateGraph` is a localized change.

## Consequences

- The loop is ~40 lines and fully readable; tests don't need a graph runtime.
- We own concerns LangGraph would provide (checkpointing, streaming, retries,
  parallel branches). When we need those, we port - ADR to follow.
- The node functions already take `(deps, state)`, which maps cleanly onto
  LangGraph nodes, so the migration cost is contained.

## Alternatives considered

- **Adopt LangGraph now** - best long-term, but heavier deps and a steeper read for
  a template whose job is to be understood. Deferred, not rejected.
- **A generic agent framework (CrewAI, Autogen, etc.)** - more opinionated and
  heavier than the problem; would bury the architecture we're trying to showcase.
