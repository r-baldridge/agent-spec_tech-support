"""Networking specialist: TCP/IP, DNS, HTTP/TLS, firewalls, BGP."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_networking_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="networking_specialist",
        description=(
            "Specialist in TCP/IP, DNS, HTTP/TLS, firewalls, VPNs, "
            "SDN, BGP/OSPF, and load balancing diagnostics."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="networking_specialization",
            additional_instructions=DOMAIN_PROMPTS["networking"],
            additional_tools=ToolRegistry.get_many(
                "network_diagnostic", "shell_execute"
            ),
        ),
    )
