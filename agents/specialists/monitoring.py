"""Monitoring specialist: Prometheus, Grafana, ELK, Jaeger, OpenTelemetry."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_monitoring_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="monitoring_specialist",
        description=(
            "Specialist in Prometheus, Grafana, ELK, Jaeger, OpenTelemetry, "
            "SLO/SLI design, and alerting strategy."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="monitoring_specialization",
            additional_instructions=DOMAIN_PROMPTS["monitoring"],
            additional_tools=ToolRegistry.get_many("query_metrics"),
        ),
    )
