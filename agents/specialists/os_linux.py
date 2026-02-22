"""Linux OS specialist: kernel, systemd, filesystems, performance tuning."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_os_linux_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="os_linux_specialist",
        description=(
            "Specialist in Linux kernel, systemd, filesystems, process "
            "management, and performance tuning."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="os_linux_specialization",
            additional_instructions=DOMAIN_PROMPTS["os_linux"],
            additional_tools=ToolRegistry.get_many(
                "shell_execute", "audit_config"
            ),
        ),
    )
