# SENTIENCE Engineering Instructions

## Mission
SENTIENCE is an experimental artificial cognitive system. Development must preserve scientific honesty: no implementation may be described as proof of consciousness or sentience merely because it produces convincing language or behavior.

## Engineering Principles
- Prefer small, testable, reversible changes.
- Do not replace or substantially restructure architecture without documenting the decision.
- Keep subsystems modular and expose documented interfaces.
- Add tests with new functionality.
- Do not introduce external services, credentials, autonomous network access, self-replication, or unrestricted system access without explicit human approval.
- Never store secrets, API keys, passwords, tokens, or private personal information in the repository.
- Preserve reproducibility and version history.
- Record important experiments, failures, unexpected behaviors, and architectural decisions.
- Treat unexpected behavior as an observation to investigate before changing it.

## Current Phase
Phase 1: repository and architectural scaffolding. Do not implement autonomous agency, continuous operation, self-modification, or claims of sentience at this stage.

## Required Workflow
1. Inspect the existing repository before changing it.
2. Explain the intended change when a task is architecturally significant.
3. Make the smallest coherent implementation.
4. Add or update tests where applicable.
5. Run relevant tests and report their results.
6. Review the diff for accidental changes.
7. Commit completed changes with a clear message.

## Source of Truth
The repository documentation and approved architectural decisions are authoritative. If instructions conflict or are ambiguous, stop and request clarification rather than inventing a major architectural decision.
