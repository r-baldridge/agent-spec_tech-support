"""Cloud infrastructure specialist: AWS/GCP/Azure/OCI, Kubernetes, Terraform."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_cloud_infra_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="cloud_infra_specialist",
        description=(
            "Specialist in AWS, GCP, Azure, OCI, Kubernetes, Terraform, "
            "and container orchestration."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="cloud_infra_specialization",
            additional_instructions=DOMAIN_PROMPTS["cloud_infra"],
            additional_tools=ToolRegistry.get_many(
                "query_metrics", "shell_execute"
            ),
        ),
    )
