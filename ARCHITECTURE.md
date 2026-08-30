# SENTIENCE Architecture

**Version:** 0.1.0
**Status:** Initial architectural scaffold

## Purpose

This document defines the initial modular architecture for the SENTIENCE research project. It is intentionally conservative: the first implementation establishes boundaries and observability before attempting advanced cognition or autonomy.

## Initial subsystem boundaries

- `core/` — lifecycle, shared state, event definitions, and subsystem interfaces.
- `cognition/` — reasoning and cognitive orchestration interfaces.
- `memory/` — memory abstractions and later memory implementations.
- `self_model/` — persistent representation of the system itself.
- `world_model/` — representation of external entities, events, relationships, and uncertainty.
- `motivation/` — goals, priorities, and computational valence variables.
- `metacognition/` — monitoring and evaluation of the system's own cognitive processes.
- `learning/` — experience-driven state and strategy changes.
- `agency/` — action selection and permission-controlled execution.
- `perception/` — ingestion and normalization of observations.
- `interface/` — human-facing communication and future external interfaces.
- `tests/` — cross-subsystem and architectural tests.

## Development order

1. Repository scaffold and documentation.
2. Core types and event/state interfaces.
3. Deterministic tests and observability.
4. Memory foundations.
5. Self-model and world-model foundations.
6. Metacognition.
7. Motivation and learning.
8. Cognitive orchestration.
9. Permission-controlled agency.
10. Continuous processing experiments.
11. Advanced experiments and evaluation.

## Architectural constraints

The system must remain modular enough that model providers, storage implementations, and interfaces can be replaced without rewriting the cognitive architecture. The project must not assume that a particular language model is itself conscious.

No autonomous external action is part of the initial scaffold.
