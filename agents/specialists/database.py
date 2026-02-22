"""Database specialist: PostgreSQL, MySQL, Oracle, MongoDB, Redis."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_database_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="database_specialist",
        description=(
            "Specialist in PostgreSQL, MySQL, Oracle, MongoDB, and Redis "
            "administration, query optimization, replication, and data integrity."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="database_specialization",
            additional_instructions=DOMAIN_PROMPTS["database"],
            additional_tools=ToolRegistry.get_many("shell_execute"),
        ),
    )
