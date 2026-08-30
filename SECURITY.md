# SENTIENCE Security and Permission Policy

## Initial posture

SENTIENCE is a research system and must begin with minimal privileges.

The initial system must not have unrestricted ability to:

- access private personal information;
- spend money or make purchases;
- modify its own security controls;
- replicate itself;
- deploy itself to arbitrary systems;
- communicate with arbitrary external systems;
- modify production infrastructure;
- delete project history; or
- grant itself additional permissions.

## Secrets

API keys, passwords, access tokens, private keys, and other credentials must never be committed to GitHub.

Use environment variables or an approved secret-management mechanism when credentials become necessary.

## Change control

Any future increase in external access or autonomous capability requires explicit human approval and documentation in the research log.
