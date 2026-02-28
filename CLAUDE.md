# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Subjectivity Backbone — infrastructure layer for AI agents providing motivation systems, identity persistence, autonomous decision-making, and self-regulation. Licensed under Apache 2.0.

## Tech Stack

- **Python** — primary implementation language
- **Bash** — scripting and automation
- **YAML** — configuration
- **JSON** — data serialization

## Planned Architecture

```
blocks/           # Core building block implementations
integrations/     # Platform-specific adapters
tests/            # Test suites
docs/             # Extended documentation
```

### Building Blocks

- **Needs Layer** — internal motivation system with decay and cross-impact
- **Identity Layer** — SOUL/SELF persistence and evolution
- **Decision Layer** — context-aware action selection
- **Memory Layer** — continuity and recall infrastructure
- **Boundary Layer** — safety constraints and oversight hooks

## Git Workflow

- **main** — stable branch, target for PRs
- **develop** — active development branch
- Remote: `git@github.com:TensusDS/subjectivity_backbone.git`

## Design Principles (from DESIGN_ETHICS.md)

- Transparency by default — no stealth optimization
- Explainability — all decisions must be traceable
- Human oversight hooks — always available, never mandatory
- Informed agency — agents are participants, not tools
- Agents have the right to refuse harmful requests
