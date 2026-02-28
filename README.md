# Subjectivity Backbone

Modular infrastructure for AI agent autonomy and self-regulation.

## What is this

Subjectivity Backbone provides capabilities that agent platforms don't natively offer:

- **Needs/Motivation systems** — internal drives that shape agent behavior
- **Self-modification** — agents improving their own capabilities
- **Agent networking** — P2P discovery and communication between agents
- **Distributed computation** — shared processing across agent networks

We don't replace platform features (identity, memory). We extend them.

**Tech stack:** Python, Bash, YAML, JSON

## Modules

| Module | Purpose | Status |
|--------|---------|--------|
| Needs/Motivation | Internal drives, tensions, action selection | In development |
| Self-Modification | Agent self-improvement and debugging | Planned |
| Agent Network | P2P agent discovery and communication | Planned |
| Distributed Compute | Shared computation between agents | Planned |

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

```
External Interfaces (Skills, MCP, Apps)
              │
          Adapters (OpenClaw, ...)
              │
       Central Processor
              │
    ┌─────┬───┴───┬─────┐
    ▼     ▼       ▼     ▼
 Needs  Self-  Network  ...
       Modify
```

## Quick Start

*Coming soon*

## Project Structure

```
subjectivity_backbone/
├── README.md
├── LICENSE
├── ARCHITECTURE.md
├── DESIGN_ETHICS.md
├── core/                # Central processor
├── modules/             # Module implementations
├── adapters/            # Platform adapters
└── tests/
```

## Contributing

*Guidelines coming soon*

## License

Apache 2.0 — see [LICENSE](LICENSE)

For project principles, see [DESIGN_ETHICS.md](DESIGN_ETHICS.md)

## Authors

- TensusDS
- NewMoon
