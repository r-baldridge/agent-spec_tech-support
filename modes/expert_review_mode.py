"""Expert review mode: standalone expert reviewer as a Flow node."""

from pyagentspec.agent import Agent
from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode


def build_expert_review_flow(expert_reviewer: Agent) -> Flow:
    """Build a single-step Flow that runs the expert reviewer.

    The reviewer receives all accumulated output from triage and specialist
    work, independently verifies the diagnosis, and produces a verdict.
    """
    review_node = AgentNode(
        name="expert_review",
        description=(
            "Independent expert review of the diagnosis and remediation. "
            "Produces a verdict: APPROVED, MODIFY, REWORK, or REJECTED."
        ),
        agent=expert_reviewer,
    )

    flow = (
        FlowBuilder()
        .add_node(review_node)
        .set_entry_point(review_node)
        .set_finish_points(review_node)
        .build(name="expert_review_flow")
    )

    return flow
