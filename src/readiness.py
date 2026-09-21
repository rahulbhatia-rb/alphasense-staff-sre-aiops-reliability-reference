"""Policy-as-code gate for a production service's reliability contract."""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class Service:
    name: str
    availability_slo: float
    availability_observed: float
    error_budget_remaining_pct: float
    trace_coverage_pct: float
    profiling_enabled: bool
    runbook_tested: bool
    incident_owner: str
    open_postmortem_actions: int
    rollback_tested: bool
    paved_path_version: str
    ai_remediation_mode: str
    human_approval_required: bool

    @classmethod
    def from_dict(cls, value: Dict[str, Any]) -> "Service":
        return cls(**value)


def _finding(code: str, severity: str, remediation: str) -> Dict[str, str]:
    return {"code": code, "severity": severity, "remediation": remediation}


def assess(service: Service) -> Dict[str, Any]:
    """Return an explainable go/no-go decision using only supplied evidence."""
    findings: List[Dict[str, str]] = []
    blockers: List[str] = []

    if not 0 < service.availability_slo <= 100:
        findings.append(_finding("invalid-slo", "blocker", "Set an SLO between 0 and 100."))
        blockers.append("invalid-slo")
    elif service.availability_observed < service.availability_slo:
        findings.append(_finding("slo-missed", "blocker", "Restore observed availability above the SLO."))
        blockers.append("slo-missed")
    if service.error_budget_remaining_pct <= 0:
        findings.append(_finding("error-budget-exhausted", "blocker", "Freeze risky changes and follow the recovery plan."))
        blockers.append("error-budget-exhausted")
    elif service.error_budget_remaining_pct < 10:
        findings.append(_finding("error-budget-low", "warning", "Prioritize reliability work before increasing change velocity."))
    if service.trace_coverage_pct < 95:
        findings.append(_finding("trace-coverage-low", "blocker", "Instrument request paths until trace coverage reaches 95%."))
        blockers.append("trace-coverage-low")
    if not service.profiling_enabled:
        findings.append(_finding("continuous-profiling-missing", "warning", "Enable continuous profiling for regressions."))
    if not service.runbook_tested:
        findings.append(_finding("runbook-untested", "blocker", "Exercise the service runbook in a recovery drill."))
        blockers.append("runbook-untested")
    if not service.incident_owner.strip():
        findings.append(_finding("incident-owner-missing", "blocker", "Assign an accountable incident owner."))
        blockers.append("incident-owner-missing")
    if service.open_postmortem_actions > 0:
        findings.append(_finding("postmortem-actions-open", "warning", "Track and close corrective actions with owners and due dates."))
    if not service.rollback_tested:
        findings.append(_finding("rollback-untested", "blocker", "Prove rollback for the deployment strategy."))
        blockers.append("rollback-untested")
    if not service.paved_path_version.strip():
        findings.append(_finding("paved-path-missing", "blocker", "Adopt a supported platform template/version."))
        blockers.append("paved-path-missing")
    if service.ai_remediation_mode not in {"disabled", "advisory", "approved-execution"}:
        findings.append(_finding("invalid-ai-remediation-mode", "blocker", "Use disabled, advisory, or approved-execution."))
        blockers.append("invalid-ai-remediation-mode")
    if service.ai_remediation_mode == "approved-execution" and not service.human_approval_required:
        findings.append(_finding("ai-remediation-not-approved", "blocker", "Require human approval before remediation execution."))
        blockers.append("ai-remediation-not-approved")

    warnings = sum(item["severity"] == "warning" for item in findings)
    score = max(0, 100 - (35 * len(blockers)) - (5 * warnings))
    return {"service": asdict(service), "production_ready": not blockers, "readiness_score": score, "blockers": blockers, "findings": findings}
