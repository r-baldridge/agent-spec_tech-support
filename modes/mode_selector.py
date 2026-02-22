"""Context-based mode selection logic.

Determines which operational mode to activate based on issue characteristics.
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class OperationalMode(str, Enum):
    """Available operational modes for issue resolution."""

    MANAGER = "manager"
    SPECIALIST_WORKFLOW = "specialist_workflow"
    SWARM = "swarm"
    EXPERT_REVIEW = "expert_review"


@dataclass
class ModeSelection:
    """Result of mode selection."""

    mode: OperationalMode
    primary_domain: str
    peer_domains: List[str]
    severity: str
    rationale: str


def select_mode(
    domain: str,
    severity: str,
    cross_domain: bool = False,
    peer_domains: Optional[List[str]] = None,
    specialist_resolved: bool = False,
) -> ModeSelection:
    """Select the appropriate operational mode based on issue context.

    Parameters
    ----------
    domain:
        Primary technical domain of the issue.
    severity:
        Severity level (P1, P2, P3, P4).
    cross_domain:
        Whether the issue spans multiple technical domains.
    peer_domains:
        Additional domains involved, if cross_domain is True.
    specialist_resolved:
        Whether a specialist has already resolved the issue (for review mode).
    """
    peers = peer_domains or []

    if specialist_resolved:
        return ModeSelection(
            mode=OperationalMode.EXPERT_REVIEW,
            primary_domain=domain,
            peer_domains=peers,
            severity=severity,
            rationale="Specialist work complete; routing to expert review.",
        )

    if severity == "P1" or (cross_domain and len(peers) >= 2):
        return ModeSelection(
            mode=OperationalMode.SWARM,
            primary_domain=domain,
            peer_domains=peers,
            severity=severity,
            rationale=(
                f"Severity {severity} with {len(peers)} cross-domain dependencies "
                "requires coordinated swarm response."
            ),
        )

    if cross_domain and peers:
        return ModeSelection(
            mode=OperationalMode.SWARM,
            primary_domain=domain,
            peer_domains=peers,
            severity=severity,
            rationale="Cross-domain issue requires swarm collaboration.",
        )

    return ModeSelection(
        mode=OperationalMode.MANAGER,
        primary_domain=domain,
        peer_domains=[],
        severity=severity,
        rationale=f"Single-domain {severity} issue; delegating via manager mode.",
    )
