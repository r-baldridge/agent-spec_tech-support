"""Change validation Flow: pre/post change verification.

Stages: pre_check -> apply_change -> post_check -> compare
"""

from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode, LlmNode
from pyagentspec.llms import LlmConfig
from pyagentspec.specialized_agent import SpecializedAgent


def build_change_validation_flow(
    specialist: SpecializedAgent,
    analysis_llm_config: LlmConfig,
) -> Flow:
    """Build a pre/post change validation Flow.

    This ensures changes are validated by capturing system state before
    and after the change, then comparing to detect regressions.
    """
    pre_check_node = AgentNode(
        name="pre_change_check",
        description=(
            "Capture the current system state before applying the change. "
            "Record metrics, service health, and configuration baselines."
        ),
        agent=specialist,
    )

    apply_change_node = AgentNode(
        name="apply_change",
        description=(
            "Apply the planned change with appropriate safety measures "
            "(canary, blue-green, or direct depending on risk level)."
        ),
        agent=specialist,
    )

    post_check_node = AgentNode(
        name="post_change_check",
        description=(
            "Capture system state after the change. Check service health, "
            "verify expected improvements, and detect any regressions."
        ),
        agent=specialist,
    )

    compare_node = LlmNode(
        name="change_comparison",
        description="Compare pre and post states to validate the change",
        llm_config=analysis_llm_config,
        prompt_template=(
            "Compare the following pre-change and post-change system states.\n"
            "Identify: improvements, regressions, unexpected changes, and "
            "whether the change objective was achieved.\n\n"
            "Pre-change state:\n{{pre_state}}\n\n"
            "Post-change state:\n{{post_state}}"
        ),
    )

    flow = (
        FlowBuilder()
        .add_sequence([pre_check_node, apply_change_node, post_check_node, compare_node])
        .set_entry_point(pre_check_node)
        .set_finish_points(compare_node)
        .build(name="change_validation_flow")
    )

    return flow
