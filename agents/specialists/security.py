"""Security specialist: TLS/PKI, RBAC, incident response, forensics."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_security_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="security_specialist",
        description=(
            "Specialist in TLS/PKI, RBAC, secrets management, vulnerability "
            "scanning, incident response, and digital forensics."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="security_specialization",
            additional_instructions=DOMAIN_PROMPTS["security"],
            additional_tools=ToolRegistry.get_many(
                "shell_execute", "audit_config"
            ),
        ),
    )
