"""CI/CD specialist: Jenkins, GitLab CI, GitHub Actions, ArgoCD, Tekton."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_cicd_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="cicd_specialist",
        description=(
            "Specialist in Jenkins, GitLab CI, GitHub Actions, ArgoCD, "
            "Tekton, build optimization, and deployment pipelines."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="cicd_specialization",
            additional_instructions=DOMAIN_PROMPTS["cicd"],
            additional_tools=ToolRegistry.get_many("shell_execute"),
        ),
    )
