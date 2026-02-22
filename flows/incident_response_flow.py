"""Incident response Flow: incident lifecycle management.

Stages:
  detect -> assess -> contain -> investigate -> remediate -> verify -> document
"""

from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode, LlmNode
from pyagentspec.llms import LlmConfig
from pyagentspec.specialized_agent import SpecializedAgent


def build_incident_response_flow(
    specialist: SpecializedAgent,
    analysis_llm_config: LlmConfig,
) -> Flow:
    """Build an incident lifecycle Flow.

    This follows the structured incident response process:
    assess -> contain -> investigate -> remediate -> verify
    """
    assess_node = AgentNode(
        name="incident_assessment",
        description=(
            "Assess the incident: determine blast radius, affected users, "
            "business impact, and initial severity classification."
        ),
        agent=specialist,
    )

    contain_node = AgentNode(
        name="incident_containment",
        description=(
            "Apply immediate containment measures to stop the bleeding. "
            "Isolate affected systems, enable fallbacks, or apply temporary mitigations."
        ),
        agent=specialist,
    )

    investigate_node = AgentNode(
        name="incident_investigation",
        description=(
            "Deep investigation to identify root cause. Gather evidence, "
            "correlate logs and metrics, trace the failure path."
        ),
        agent=specialist,
    )

    rca_node = LlmNode(
        name="root_cause_synthesis",
        description="Synthesise investigation findings into a formal root cause analysis",
        llm_config=analysis_llm_config,
        prompt_template=(
            "Based on the following investigation findings, produce a formal "
            "root cause analysis (RCA).\n\n"
            "Include: timeline, contributing factors, root cause, impact summary, "
            "and recommended preventive measures.\n\n"
            "{{investigation_findings}}"
        ),
    )

    remediate_node = AgentNode(
        name="incident_remediation",
        description="Apply the definitive fix and verify the system is restored",
        agent=specialist,
    )

    verify_node = AgentNode(
        name="incident_verification",
        description=(
            "Verify the fix is effective: check metrics, run smoke tests, "
            "confirm no regressions, and validate SLIs are back to normal."
        ),
        agent=specialist,
    )

    flow = (
        FlowBuilder()
        .add_sequence([
            assess_node,
            contain_node,
            investigate_node,
            rca_node,
            remediate_node,
            verify_node,
        ])
        .set_entry_point(assess_node)
        .set_finish_points(verify_node)
        .build(name="incident_response_flow")
    )

    return flow
