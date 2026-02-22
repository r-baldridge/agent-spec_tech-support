"""Domain -> specialist lookup registry."""

from typing import Dict, List

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import SpecializedAgent

from agents.specialists.networking import create_networking_specialist
from agents.specialists.database import create_database_specialist
from agents.specialists.os_linux import create_os_linux_specialist
from agents.specialists.cloud_infra import create_cloud_infra_specialist
from agents.specialists.application_code import create_application_code_specialist
from agents.specialists.security import create_security_specialist
from agents.specialists.cicd import create_cicd_specialist
from agents.specialists.monitoring import create_monitoring_specialist


class SpecialistRegistry:
    """Registry mapping domain names to specialist factory functions.

    Call :meth:`build_all` with a base agent to instantiate every specialist.
    """

    _FACTORIES = {
        "networking": create_networking_specialist,
        "database": create_database_specialist,
        "os_linux": create_os_linux_specialist,
        "cloud_infra": create_cloud_infra_specialist,
        "application_code": create_application_code_specialist,
        "security": create_security_specialist,
        "cicd": create_cicd_specialist,
        "monitoring": create_monitoring_specialist,
    }

    @classmethod
    def domains(cls) -> List[str]:
        """Return all registered domain names."""
        return list(cls._FACTORIES.keys())

    @classmethod
    def build(cls, domain: str, base_agent: Agent) -> SpecializedAgent:
        """Build a single specialist for the given domain."""
        factory = cls._FACTORIES.get(domain)
        if factory is None:
            raise KeyError(
                f"Unknown domain '{domain}'. "
                f"Available: {', '.join(cls._FACTORIES)}"
            )
        return factory(base_agent)

    @classmethod
    def build_all(cls, base_agent: Agent) -> Dict[str, SpecializedAgent]:
        """Build all specialists from the given base agent."""
        return {
            domain: factory(base_agent)
            for domain, factory in cls._FACTORIES.items()
        }

    @classmethod
    def build_all_list(cls, base_agent: Agent) -> List[SpecializedAgent]:
        """Build all specialists as an ordered list."""
        return [factory(base_agent) for factory in cls._FACTORIES.values()]
