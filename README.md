# AlphaSense Staff SRE — AIOps reliability paved path

A runnable, policy-as-code proof of concept for a Staff SRE operating model: make safe production delivery self-service, preserve product-team ownership, and treat AI remediation as a controlled engineering capability.

## What it evaluates

Each JSON service contract yields an explainable deployment decision.

| Control | Evidence | Decision |
| --- | --- | --- |
| Reliability objective | SLO and observed availability | Missed SLO blocks readiness |
| Change safety | Error-budget remaining percentage | Exhausted budget blocks risky rollout |
| Observability | Request-trace coverage and profiling | Trace coverage below 95% blocks readiness |
| Operations | Tested runbook and named incident owner | Missing evidence blocks readiness |
| Learning | Outstanding postmortem actions | Visible warning with corrective work |
| Recovery | Tested rollback | Missing proof blocks readiness |
| Platform adoption | Paved-path version | Unsupported/unversioned path blocks readiness |
| AIOps | Mode plus approval policy | Autonomous execution without human approval blocks readiness |

The result includes structured `blockers`, `findings`, a `readiness_score`, and the input evidence. It can power a pull-request check, Backstage scorecard, or deployment approval view.

## Run it

```bash
python3 -m unittest discover -s tests -v
python3 -m src.app < examples/services.jsonl
```

The stream includes one approved service and one deliberately unsafe service. It shows that an AIOps agent cannot turn an unhealthy service into an approved deployment simply by proposing an action.

## Architecture

```text
Prometheus / SLO store ─┐
OpenTelemetry / profiles ├─> evidence collector ─> readiness policy ─> PR / deploy gate
Incident & postmortems ─┤                                  │
Platform templates ─────┘                                  └─> scorecard + remediation guidance

AI diagnostics ─> evidence and proposed plan ─> policy checks ─> explicit human approval ─> executable change
                                                                    │
                                                             verified rollback
```

## Production implementation

1. Publish versioned service templates that create telemetry, ownership, runbook, rollback, and deployment contracts by default.
2. Ingest quantitative evidence from observability, incident, deployment, and profiling systems rather than spreadsheet self-attestation.
3. Evaluate policy on pull requests and before promotion. Each failure returns a stable code and a specific remediation.
4. AI may summarize telemetry and draft a remediation plan; it cannot bypass change policy or acquire production credentials.
5. A human approves the proposed action, confirms rollback, and the delivery system records approval and outcome for auditability.

The aim is not to centralize every operational decision in SRE. It is to give engineers a fast paved path and make reliability debt visible before it becomes an incident.
