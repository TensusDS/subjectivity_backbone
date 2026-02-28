# Architecture

## Overview

Subjectivity Backbone is a modular infrastructure layer for AI agent autonomy. It provides capabilities that platforms (like OpenClaw) don't natively offer, without replacing existing platform features.

## Design Principle

**We don't define WHO the agent is — that's the agent's domain.**

We provide:
- Ethical framework (DESIGN_ETHICS.md)
- Infrastructure for autonomous capabilities

## Layer Structure

```
                    ┌─────────────────────────┐
                    │   External Interfaces   │
                    │  Skills, MCP, Apps...   │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │        Adapters         │
                    │  OpenClaw, Claude, ...  │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │    Central Processor    │
                    │   (Orchestration Hub)   │
                    └───────────┬─────────────┘
                                │
    ┌───────────┬───────────────┼───────────────┬───────────┐
    ▼           ▼               ▼               ▼           ▼
┌───────┐ ┌───────────┐ ┌─────────────┐ ┌───────────┐ ┌─────┐
│Needs/ │ │   Self-   │ │   Agent     │ │Distributed│ │ ... │
│Motiv. │ │  Modify   │ │  Network    │ │  Compute  │ │     │
└───────┘ └───────────┘ └─────────────┘ └───────────┘ └─────┘
```

## Components

### Central Processor

Orchestration hub that:
- Loads enabled modules
- Routes data between modules
- Provides unified API for adapters
- Manages module lifecycle

### Modules (Core)

| Module | Purpose | Status |
|--------|---------|--------|
| **Needs/Motivation** | Internal drives, tensions, action selection (Turing Pyramid) | Reference implementation exists |
| **Self-Modification** | Agent self-improvement, debugging, code evolution | Planned |
| **Agent Network** | P2P discovery, agent-to-agent communication | Planned |
| **Distributed Compute** | Shared computation, task delegation between agents | Planned |

### Adapters

Bridge between Central Processor and external platforms.

**Adapter responsibilities:**
```python
class Adapter:
    def get_workspace(self) -> Path
        """Where modules store their state"""
    
    def get_identity(self) -> dict | None
        """Read-only access to agent identity (if needed)"""
    
    def get_memory(self) -> dict | None
        """Read-only access to agent memory (if needed)"""
    
    def trigger_action(self, action: str) -> bool
        """Request agent to perform action"""
    
    def on_heartbeat(self) -> None
        """Called on agent heartbeat/cycle"""
```

**Planned adapters:**
- OpenClaw (primary)
- MCP Server (for external access/monitoring)
- Future platforms

## What Backbone Does NOT Do

- ❌ Manage agent identity (platform responsibility)
- ❌ Manage agent memory (platform responsibility)  
- ❌ Replace platform features
- ❌ Force specific behaviors

## Module Interface

All modules implement a standard interface:

```python
class Module:
    def __init__(self, processor: CentralProcessor)
    
    def evaluate(self, context: dict) -> ModuleResult
        """Run module logic, return results"""
    
    def update(self, action: str, params: dict) -> bool
        """Update module state based on action"""
    
    def get_state(self) -> dict
        """Return current module state"""
```

## Data Flow

```
Heartbeat/Trigger
       │
       ▼
   Adapter
       │
       ▼
Central Processor
       │
       ├──► Module A ──► result
       ├──► Module B ──► result
       └──► Module C ──► result
       │
       ▼
  Aggregate Results
       │
       ▼
   Adapter
       │
       ▼
Agent Decision/Action
```

## Tech Stack

- **Core:** Python
- **Integration:** Bash wrappers
- **Config/State:** YAML, JSON
- **Testing:** pytest

---

*Version: 0.1 | Last updated: 2026-02-28*
