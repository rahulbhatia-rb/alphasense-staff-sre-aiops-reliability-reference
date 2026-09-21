from dataclasses import dataclass,asdict
from typing import Any
@dataclass(frozen=True)
class Service:
 slo_defined:bool; error_budget_healthy:bool; metrics_logs_traces:bool; profiling_enabled:bool; runbook_tested:bool; incident_owner_assigned:bool; postmortem_action_items_tracked:bool; ai_remediation_human_approval:bool; rollback_tested:bool; paved_path_adopted:bool
 @classmethod
 def from_dict(cls,v:dict[str,Any])->"Service":return cls(**v)
def assess(s:Service)->dict[str,Any]:
 c={"slo-missing":s.slo_defined,"error-budget-exhausted":s.error_budget_healthy,"observability-incomplete":s.metrics_logs_traces,"continuous-profiling-missing":s.profiling_enabled,"runbook-untested":s.runbook_tested,"incident-owner-missing":s.incident_owner_assigned,"postmortem-actions-untracked":s.postmortem_action_items_tracked,"ai-remediation-not-approved":s.ai_remediation_human_approval,"rollback-untested":s.rollback_tested,"paved-path-not-adopted":s.paved_path_adopted}
 f=[k for k,v in c.items() if not v];return {"production_ready":not f,"findings":f,"service":asdict(s)}
