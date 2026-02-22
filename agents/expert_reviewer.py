"""Expert reviewer agent: final quality gate for all diagnostic work."""

from pyagentspec.agent import Agent
from pyagentspec.llms import LlmConfig

from knowledge.domain_prompts import EXPERT_REVIEWER_PROMPT
from tools.tool_registry import ToolRegistry


def create_expert_reviewer(llm_config: LlmConfig) -> Agent:
    """Create the expert reviewer agent.

    The reviewer independently verifies diagnoses, validates remediations,
    and produces a final verdict with risk rating.
    """
    return Agent(
        name="expert_reviewer",
        description=(
            "Expert reviewer that independently verifies diagnoses, validates "
            "remediations, and produces a final quality verdict."
        ),
        system_prompt=EXPERT_REVIEWER_PROMPT,
        llm_config=llm_config,
        tools=ToolRegistry.get_many(
            "shell_read_only",
            "knowledge_search",
            "incident_history_search",
            "query_tickets",
            "update_ticket",
            "check_alerts",
            "search_logs",
            "audit_config",
            "resource_monitor",
            "query_metrics",
        ),
        human_in_the_loop=True,
    )
