"""Triage manager agent: domain classification, severity assessment, delegation."""

from pyagentspec.agent import Agent
from pyagentspec.llms import LlmConfig

from knowledge.domain_prompts import TRIAGE_MANAGER_PROMPT
from tools.tool_registry import ToolRegistry


def create_triage_manager(llm_config: LlmConfig) -> Agent:
    """Create the triage manager agent.

    The manager analyzes incoming issues, classifies them by domain and
    severity, and delegates work to the appropriate specialist.
    """
    return Agent(
        name="triage_manager",
        description=(
            "Triage manager that classifies incoming technical issues by "
            "domain and severity, then delegates to the appropriate specialist."
        ),
        system_prompt=TRIAGE_MANAGER_PROMPT,
        llm_config=llm_config,
        tools=ToolRegistry.get_many(
            "knowledge_search",
            "query_tickets",
            "check_alerts",
            "create_ticket",
            "update_ticket",
        ),
        human_in_the_loop=True,
    )
