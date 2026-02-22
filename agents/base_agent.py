"""Base agent: shared system prompt and universal tool set for all specialists."""

from pyagentspec.agent import Agent
from pyagentspec.llms import LlmConfig

from knowledge.domain_prompts import BASE_SYSTEM_PROMPT
from tools.tool_registry import ToolRegistry


# Universal tools available to every specialist via the base agent.
_UNIVERSAL_TOOL_NAMES = [
    "shell_read_only",
    "knowledge_search",
    "incident_history_search",
    "query_tickets",
    "check_alerts",
    "search_logs",
    "resource_monitor",
]


def create_base_agent(llm_config: LlmConfig) -> Agent:
    """Create the generic base agent that all specialists extend.

    The base agent carries the universal diagnostic methodology prompt
    and the set of tools common to every domain.
    """
    return Agent(
        name="tech_support_base_agent",
        description=(
            "Generic tech support agent with universal diagnostic methodology "
            "and read-only investigation tools."
        ),
        system_prompt=BASE_SYSTEM_PROMPT,
        llm_config=llm_config,
        tools=ToolRegistry.get_many(*_UNIVERSAL_TOOL_NAMES),
        human_in_the_loop=True,
    )
