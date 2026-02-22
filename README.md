# Tech Support Agent System

An adaptive, multi-modal tech support agent system built on [Oracle's Agent Spec](https://github.com/oracle/agent-spec) framework (`pyagentspec`). Designed for hybrid engineering environments covering full-stack software dev, DevOps, infrastructure, networking, hardware/firmware, and systems administration.

The system supports multiple operational modes that activate as needed — from a single specialist handling a routine issue, to a full swarm of cross-domain experts tackling a P1 outage, with an expert reviewer as the final quality gate on all work.

## Architecture

```
Incoming Issue
     │
     ▼
┌─────────────┐
│   TRIAGE     │  ManagerWorkers pattern
│   MANAGER    │  Analyzes domain, severity, urgency
└──────┬──────┘
       │ delegates to
       ▼
┌─────────────────────┐
│  DOMAIN SPECIALIST  │  SpecializedAgent (1 of 8 domains)
│  (single or primary)│
└──────┬──────────────┘
       │ can resolve directly, or escalate:
       ├──► Structured Workflow (Flow)     ── for methodical diagnostics
       ├──► Swarm (with approval)          ── for cross-domain problems
       │
       ▼
┌─────────────────────┐
│   EXPERT REVIEWER   │  Final quality gate
│                     │  Verdict: APPROVED / MODIFY / REWORK / REJECTED
└─────────────────────┘
```

## Operational Modes

| Mode | Pattern | When |
|------|---------|------|
| **Manager** | `ManagerWorkers` | Single-domain issues — manager triages, delegates to one specialist |
| **Specialist Workflow** | `Flow` | Structured diagnostics — plan → collect → analyze → remediate |
| **Swarm** | `Swarm` (OPTIONAL handoff) | Cross-domain P1 incidents — fully-connected specialist collaboration |
| **Expert Review** | Standalone `Agent` | Final quality gate on all completed work |

## Domain Specialists

Eight `SpecializedAgent` instances, each carrying deep domain expertise:

| Specialist | Scope | Additional Tools |
|-----------|-------|-----------------|
| **Networking** | TCP/IP, DNS, HTTP/TLS, firewalls, BGP/OSPF, VPNs, SDN | `network_diagnostic`, `shell_execute` |
| **Database** | PostgreSQL, MySQL, Oracle, MongoDB, Redis, replication | `shell_execute` |
| **Linux OS** | Kernel, systemd, filesystems, performance tuning | `shell_execute`, `audit_config` |
| **Cloud Infra** | AWS/GCP/Azure/OCI, Kubernetes, Terraform, containers | `query_metrics`, `shell_execute` |
| **Application Code** | Debugging, profiling, memory leaks (Python/Java/Go/Node/Rust/C++) | `shell_execute`, `search_logs` |
| **Security** | TLS/PKI, RBAC, secrets, vulnerability scanning, incident response | `shell_execute`, `audit_config` |
| **CI/CD** | Jenkins, GitLab CI, GitHub Actions, ArgoCD, Tekton | `shell_execute` |
| **Monitoring** | Prometheus, Grafana, ELK, Jaeger, OpenTelemetry, SLO/SLI | `query_metrics` |

All specialists share a base agent with 7 universal read-only tools: `shell_read_only`, `knowledge_search`, `incident_history_search`, `query_tickets`, `check_alerts`, `search_logs`, `resource_monitor`.

## Tools

13 `ServerTool` definitions with typed `Property` schemas:

| Tool | Confirmation | Purpose |
|------|:---:|---------|
| `shell_execute` | Yes | Execute commands (write ops need approval) |
| `shell_read_only` | No | Safe read-only system commands |
| `knowledge_search` | No | Search docs, runbooks, guides |
| `incident_history_search` | No | Find similar past incidents |
| `create_ticket` | Yes | Create new support tickets |
| `update_ticket` | No | Add comments/status updates |
| `query_tickets` | No | Search existing tickets |
| `query_metrics` | No | PromQL / metric queries |
| `check_alerts` | No | Current alert state |
| `search_logs` | No | Log search (ELK/Loki/CloudWatch) |
| `audit_config` | No | Configuration file analysis |
| `network_diagnostic` | No | ping, traceroute, DNS, TLS checks |
| `resource_monitor` | No | CPU, memory, disk, processes |

## Flows

Four reusable `Flow` pipelines:

- **Diagnostic Flow** — plan → collect → analyze → remediate (wrapped in `CatchExceptionNode`)
- **Incident Response Flow** — assess → contain → investigate → RCA → remediate → verify
- **Change Validation Flow** — pre-check → apply → post-check → compare
- **Escalation Flow** — specialist attempt → escalation decision → swarm → expert review

## Safety & Guardrails

- `requires_confirmation` on `shell_execute` and `create_ticket`
- `human_in_the_loop=True` on all agents
- **Command allowlist** — read-only commands safe; destructive commands require confirmation; dangerous commands blocked
- **Swarm approval gate** — manager must approve; resource limits enforced (max 3 concurrent swarms, max 5 agents per swarm)
- **`CatchExceptionNode`** wraps risky subflows for graceful degradation
- **Audit trail** — custom `SpanProcessor` logs all tool invocations and agent decisions to JSONL

## LLM Configuration

Multi-provider support via `OpenAiCompatibleConfig`:

| Profile | Role | Model |
|---------|------|-------|
| `claude/default` | Manager, Reviewer | claude-sonnet-4 via LiteLLM proxy |
| `openai/default` | Specialists | gpt-4o |
| `ollama/fast` | Simple tool selection | llama3.1:70b local |
| `vllm/large` | On-prem sensitive data | Qwen2.5-72B on internal vLLM |

## Project Structure

```
tech-support-agent/
├── pyproject.toml
├── config/                  # LLM profiles, settings, safety policy
├── agents/                  # Base agent, triage manager, expert reviewer
│   └── specialists/         # 8 domain specialists
├── tools/                   # 13 ServerTool definitions + registry
├── modes/                   # Manager, specialist workflow, swarm, orchestrator
├── flows/                   # Diagnostic, incident response, change validation, escalation
├── safety/                  # Command allowlist, approval gate, resource limiter, audit
├── knowledge/               # Domain expertise system prompts
├── specs/                   # Generated YAML specs (26 files)
├── scripts/                 # Spec generation and validation
└── tests/                   # 217 tests
```

## Getting Started

### Prerequisites

- Python 3.10+
- [pyagentspec](https://github.com/oracle/agent-spec) installed

### Install

```bash
pip install -e /path/to/agent-spec/pyagentspec
pip install -e .
```

### Run Tests

```bash
pytest tests/ -v
```

### Generate YAML Specs

```bash
python scripts/generate_specs.py
python scripts/validate_specs.py
```

## Configuration

Set environment variables to configure LLM endpoints:

```bash
export LITELLM_PROXY_URL="http://localhost:4000/v1"
export LITELLM_API_KEY="your-key"
export OPENAI_API_KEY="your-key"
export OLLAMA_URL="http://localhost:11434"
export VLLM_URL="http://localhost:8000"
```

Swarm limits and audit logging are also configurable via environment variables — see `config/settings.py`.
