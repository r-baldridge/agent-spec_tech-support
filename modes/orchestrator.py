"""Top-level orchestration Flow.

Assembles the complete system as a Flow:
  StartNode(user_request)
    -> AgentNode(triage_manager_workers)
    -> BranchingNode(escalation_check)
        |-- "resolved" -> AgentNode(expert_reviewer) -> EndNode
        |-- "swarm_needed" -> AgentNode(swarm_placeholder) -> AgentNode(expert_reviewer) -> EndNode
        |-- "default" -> AgentNode(expert_reviewer) -> EndNode
"""

from pyagentspec.agent import Agent
from pyagentspec.flows.flow import Flow
from pyagentspec.flows.flowbuilder import FlowBuilder
from pyagentspec.flows.nodes import AgentNode, LlmNode
from pyagentspec.llms import LlmConfig
from pyagentspec.managerworkers import ManagerWorkers


def build_orchestrator(
    manager_workers: ManagerWorkers,
    expert_reviewer: Agent,
    escalation_llm_config: LlmConfig,
) -> Flow:
    """Build the top-level orchestration Flow.

    This Flow ties together triage, specialist work, escalation decisions,
    and expert review into a single end-to-end workflow.

    Parameters
    ----------
    manager_workers:
        The ManagerWorkers component (triage manager + all specialists).
    expert_reviewer:
        The expert reviewer agent.
    escalation_llm_config:
        LLM config for the escalation decision node.
    """
    # 1. Triage + specialist work via ManagerWorkers
    triage_node = AgentNode(
        name="triage_and_investigate",
        description=(
            "Triage manager analyses the issue, delegates to the appropriate "
            "specialist, and coordinates the investigation."
        ),
        agent=manager_workers,
    )

    # 2. Escalation decision — LLM node that reads the triage output
    #    and decides: "resolved", "swarm_needed", or "needs_review"
    escalation_node = LlmNode(
        name="escalation_check",
        description=(
            "Analyse triage and specialist output to determine if the issue "
            "is resolved, needs swarm escalation, or is ready for review."
        ),
        llm_config=escalation_llm_config,
        prompt_template=(
            "Based on the following investigation results, determine the next step.\n"
            "Respond with EXACTLY one word: 'resolved', 'swarm_needed', or 'needs_review'.\n\n"
            "Investigation results:\n{{investigation_output}}"
        ),
    )

    # 3. Expert review node (used on all terminal branches)
    review_node = AgentNode(
        name="expert_review",
        description="Independent expert review and final verdict",
        agent=expert_reviewer,
    )

    # 4. Swarm work node (for escalated issues — placeholder that gets
    #    replaced at runtime with the actual swarm)
    swarm_review_node = AgentNode(
        name="post_swarm_review",
        description="Expert review after swarm collaboration",
        agent=expert_reviewer,
    )

    # Build the flow using FlowBuilder
    builder = FlowBuilder()

    # Add all nodes
    builder.add_node(triage_node)
    builder.add_node(escalation_node)
    builder.add_node(review_node)
    builder.add_node(swarm_review_node)

    # Set entry point
    builder.set_entry_point(triage_node)

    # Triage -> escalation check
    builder.add_edge(triage_node, escalation_node)

    # Conditional branching based on escalation decision
    builder.add_conditional(
        source_node=escalation_node,
        source_value=LlmNode.DEFAULT_OUTPUT,
        destination_map={
            "resolved": "expert_review",
            "swarm_needed": "post_swarm_review",
        },
        default_destination="expert_review",
        branching_node_name="escalation_branch",
    )

    # Set finish points
    builder.set_finish_points([review_node, swarm_review_node])

    return builder.build(name="tech_support_orchestrator")
