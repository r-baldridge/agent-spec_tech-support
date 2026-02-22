"""Generic diagnostic Flow: plan -> collect -> analyze -> remediate.

A reusable four-stage pipeline that any specialist can use.
"""

from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode, CatchExceptionNode, LlmNode
from pyagentspec.llms import LlmConfig
from pyagentspec.property import StringProperty
from pyagentspec.specialized_agent import SpecializedAgent


def build_diagnostic_flow(
    specialist: SpecializedAgent,
    analysis_llm_config: LlmConfig,
) -> Flow:
    """Build a generic diagnostic Flow wrapped in a CatchExceptionNode.

    The inner flow follows: plan -> collect -> analyze -> remediate.
    The outer CatchExceptionNode catches exceptions from any stage and
    returns a sanitised error description instead of crashing.
    """
    # Inner flow stages
    plan_node = AgentNode(
        name="diagnostic_plan",
        description="Analyse symptoms and create a structured diagnostic plan",
        agent=specialist,
    )

    collect_node = AgentNode(
        name="evidence_collection",
        description="Execute diagnostic plan to gather logs, metrics, and system state",
        agent=specialist,
    )

    analyse_node = LlmNode(
        name="analysis",
        description="Synthesise evidence into root-cause analysis",
        llm_config=analysis_llm_config,
        prompt_template=(
            "Synthesise the following diagnostic evidence into a root-cause analysis.\n"
            "Include: confidence level, causal chain, affected components, and blast radius.\n\n"
            "{{evidence}}"
        ),
    )

    remediate_node = AgentNode(
        name="remediation",
        description="Propose and apply remediation based on root cause",
        agent=specialist,
    )

    inner_flow = (
        FlowBuilder()
        .add_sequence([plan_node, collect_node, analyse_node, remediate_node])
        .set_entry_point(plan_node)
        .set_finish_points(remediate_node)
        .build(name="diagnostic_inner_flow")
    )

    # Wrap in CatchExceptionNode for resilience
    catch_node = CatchExceptionNode(
        name="safe_diagnostic",
        description="Diagnostic pipeline with exception handling",
        subflow=inner_flow,
    )

    outer_flow = (
        FlowBuilder()
        .add_node(catch_node)
        .set_entry_point(catch_node)
        .set_finish_points(catch_node)
        .build(name="diagnostic_flow")
    )

    return outer_flow
