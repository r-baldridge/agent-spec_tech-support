"""Escalation Flow: specialist -> swarm -> expert review.

Progressive escalation chain when a specialist cannot resolve alone.
"""

from pyagentspec.agent import Agent
from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode, LlmNode
from pyagentspec.llms import LlmConfig
from pyagentspec.specialized_agent import SpecializedAgent
from pyagentspec.swarm import Swarm


def build_escalation_flow(
    specialist: SpecializedAgent,
    swarm: Swarm,
    expert_reviewer: Agent,
    escalation_llm_config: LlmConfig,
) -> Flow:
    """Build a progressive escalation Flow.

    Stages:
    1. Specialist attempts resolution
    2. LLM evaluates if resolved or needs escalation
    3. If unresolved -> Swarm collaboration
    4. Expert reviewer produces final verdict
    """
    specialist_node = AgentNode(
        name="specialist_attempt",
        description="Primary specialist attempts to resolve the issue",
        agent=specialist,
    )

    escalation_check_node = LlmNode(
        name="escalation_decision",
        description="Evaluate whether the specialist resolved the issue",
        llm_config=escalation_llm_config,
        prompt_template=(
            "Based on the specialist's findings below, determine if the issue "
            "is resolved or needs escalation to a cross-domain swarm.\n"
            "Respond with EXACTLY one word: 'resolved' or 'escalate'.\n\n"
            "{{specialist_findings}}"
        ),
    )

    swarm_node = AgentNode(
        name="swarm_collaboration",
        description="Cross-domain swarm collaborates on the unresolved issue",
        agent=swarm,
    )

    review_resolved_node = AgentNode(
        name="review_after_specialist",
        description="Expert review of specialist resolution",
        agent=expert_reviewer,
    )

    review_escalated_node = AgentNode(
        name="review_after_swarm",
        description="Expert review of swarm resolution",
        agent=expert_reviewer,
    )

    builder = FlowBuilder()

    builder.add_node(specialist_node)
    builder.add_node(escalation_check_node)
    builder.add_node(swarm_node)
    builder.add_node(review_resolved_node)
    builder.add_node(review_escalated_node)

    builder.set_entry_point(specialist_node)

    # specialist -> escalation check
    builder.add_edge(specialist_node, escalation_check_node)

    # Conditional: resolved -> review, escalate -> swarm -> review
    builder.add_conditional(
        source_node=escalation_check_node,
        source_value=LlmNode.DEFAULT_OUTPUT,
        destination_map={
            "resolved": "review_after_specialist",
            "escalate": "swarm_collaboration",
        },
        default_destination="review_after_specialist",
        branching_node_name="escalation_branch",
    )

    # swarm -> review
    builder.add_edge(swarm_node, review_escalated_node)

    builder.set_finish_points([review_resolved_node, review_escalated_node])

    return builder.build(name="escalation_flow")
