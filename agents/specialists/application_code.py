"""Application code specialist: debugging, profiling, memory leaks."""

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import AgentSpecializationParameters, SpecializedAgent

from knowledge.domain_prompts import DOMAIN_PROMPTS
from tools.tool_registry import ToolRegistry


def create_application_code_specialist(base_agent: Agent) -> SpecializedAgent:
    return SpecializedAgent(
        name="application_code_specialist",
        description=(
            "Specialist in application debugging, memory leak detection, "
            "profiling, and stack trace analysis across Python, Java, Go, "
            "Node.js, Rust, and C/C++."
        ),
        agent=base_agent,
        agent_specialization_parameters=AgentSpecializationParameters(
            name="application_code_specialization",
            additional_instructions=DOMAIN_PROMPTS["application_code"],
            additional_tools=ToolRegistry.get_many(
                "shell_execute", "search_logs"
            ),
        ),
    )
