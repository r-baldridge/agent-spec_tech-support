"""Specialist workflow mode: Flow-based structured diagnostics.

Builds a structured pipeline:
  plan -> evidence collection -> root cause analysis -> remediation
using AgentNode (for reasoning), ToolNode (for execution), and LlmNode (for analysis).
"""

from pyagentspec.agent import Agent
from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode, LlmNode
from pyagentspec.llms import LlmConfig
from pyagentspec.specialized_agent import SpecializedAgent


def build_specialist_workflow(
    specialist: SpecializedAgent,
    analysis_llm_config: LlmConfig,
) -> Flow:
    """Build a structured diagnostic Flow for a single specialist.

    Stages:
    1. **Plan** — The specialist analyses the issue and produces a diagnostic plan.
    2. **Collect** — The specialist gathers evidence using its tools.
    3. **Analyse** — An LLM node synthesises findings into a root-cause analysis.
    4. **Remediate** — The specialist proposes and (with confirmation) applies fixes.
    """
    plan_node = AgentNode(
        name="plan_investigation",
        description="Analyse the issue and produce a structured diagnostic plan",
        agent=specialist,
    )

    collect_node = AgentNode(
        name="collect_evidence",
        description="Execute the diagnostic plan, gathering logs, metrics, and system state",
        agent=specialist,
    )

    analyse_node = LlmNode(
        name="root_cause_analysis",
        description="Synthesise collected evidence into a root-cause analysis",
        llm_config=analysis_llm_config,
        prompt_template=(
            "Based on the following diagnostic evidence, identify the root cause "
            "of the issue. Provide your confidence level (HIGH/MEDIUM/LOW) and "
            "explain the causal chain from trigger to symptom.\n\n"
            "Evidence:\n{{evidence}}"
        ),
    )

    remediate_node = AgentNode(
        name="remediate",
        description="Propose and apply remediation based on the root cause analysis",
        agent=specialist,
    )

    flow = (
        FlowBuilder()
        .add_sequence([plan_node, collect_node, analyse_node, remediate_node])
        .set_entry_point(plan_node)
        .set_finish_points(remediate_node)
        .build(name="specialist_diagnostic_workflow")
    )

    return flow
