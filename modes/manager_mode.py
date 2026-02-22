"""Manager mode: ManagerWorkers assembly for triage and delegation."""

from pyagentspec.agent import Agent
from pyagentspec.managerworkers import ManagerWorkers
from pyagentspec.specialized_agent import SpecializedAgent

from agents.specialist_registry import SpecialistRegistry


def build_manager_workers(
    triage_manager: Agent,
    base_agent: Agent,
) -> ManagerWorkers:
    """Build a ManagerWorkers component with the triage manager and all specialists.

    The triage manager acts as the group manager, analysing incoming issues
    and delegating to the appropriate domain specialist worker.
    """
    specialists = SpecialistRegistry.build_all_list(base_agent)

    return ManagerWorkers(
        name="tech_support_manager_workers",
        description=(
            "Triage manager that classifies issues and delegates to the "
            "appropriate domain specialist."
        ),
        group_manager=triage_manager,
        workers=specialists,
    )


def build_manager_workers_from_specialists(
    triage_manager: Agent,
    specialists: list[SpecializedAgent],
) -> ManagerWorkers:
    """Build a ManagerWorkers from an explicit list of specialists."""
    return ManagerWorkers(
        name="tech_support_manager_workers",
        description=(
            "Triage manager that classifies issues and delegates to the "
            "appropriate domain specialist."
        ),
        group_manager=triage_manager,
        workers=specialists,
    )
