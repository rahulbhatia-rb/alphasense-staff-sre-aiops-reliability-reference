# AlphaSense Staff SRE — AIOps reliability paved path

Runnable service-readiness control for a mission-critical SaaS platform. It blocks production readiness when SLO/error-budget, OTEL observability, continuous profiling, incident command, postmortem learning, rollback, paved-path adoption, or human-approved AI remediation is missing.

## Run
python3 -m unittest discover -s tests -v

python3 -m src.app < examples/services.jsonl

## Production design

Implement a self-service scorecard fed by Prometheus/Grafana/Datadog metrics, OpenTelemetry traces, profile data, deployment evidence, and incident records. Require a service owner and error budget before onboarding. Treat AI diagnostics as advisory; automation may collect evidence and propose actions, but change execution requires policy checks, explicit approval, and a verified rollback. Standardize those controls in templates and golden paths so product teams own reliability without rebuilding SRE mechanics.
