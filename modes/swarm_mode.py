"""Swarm mode: dynamic Swarm assembly with approval gate.

Builds a Swarm from a primary specialist and requested peer specialists,
with fully-connected relationships and OPTIONAL handoff mode.
"""

from typing import List, Optional

from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import SpecializedAgent
from pyagentspec.swarm import HandoffMode, Swarm

from agents.specialist_registry import SpecialistRegistry
from safety.approval_gate import SwarmApprovalGate
from safety.resource_limiter import ResourceLimiter


def build_swarm(
    primary_domain: str,
    peer_domains: List[str],
    base_agent: Agent,
    approval_gate: Optional[SwarmApprovalGate] = None,
    resource_limiter: Optional[ResourceLimiter] = None,
) -> Swarm:
    """Build a cross-domain Swarm for complex, multi-domain issues.

    Parameters
    ----------
    primary_domain:
        Domain of the lead specialist (e.g., ``"networking"``).
    peer_domains:
        Domains of peer specialists to include (e.g., ``["security", "cloud_infra"]``).
    base_agent:
        The base agent used to construct each specialist.
    approval_gate:
        Optional approval gate.  When provided, ``approve()`` is called before
        the swarm is assembled.  Raises if denied.
    resource_limiter:
        Optional resource limiter to enforce concurrency constraints.
    """
    all_domains = [primary_domain] + [d for d in peer_domains if d != primary_domain]

    if approval_gate is not None:
        approval_gate.approve(domains=all_domains)

    if resource_limiter is not None:
        resource_limiter.check_swarm_limits(agent_count=len(all_domains))

    specialists: List[SpecializedAgent] = [
        SpecialistRegistry.build(domain, base_agent) for domain in all_domains
    ]

    primary = specialists[0]

    # Fully-connected relationships: every pair can communicate
    relationships = []
    for i, caller in enumerate(specialists):
        for j, recipient in enumerate(specialists):
            if i != j:
                relationships.append((caller, recipient))

    return Swarm(
        name=f"swarm_{'_'.join(all_domains)}",
        description=(
            f"Cross-domain swarm led by {primary_domain} specialist "
            f"with peers: {', '.join(peer_domains)}"
        ),
        first_agent=primary,
        relationships=relationships,
        handoff=HandoffMode.OPTIONAL,
    )
