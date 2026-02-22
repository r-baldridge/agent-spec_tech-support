"""Swarm approval gate: manager must approve swarm creation."""

from typing import Callable, List, Optional

from config.settings import Settings


class SwarmApprovalGate:
    """Gate that controls swarm creation.

    Before a swarm is assembled, the gate checks:
    1. The requesting domains are valid.
    2. An optional human/manager approval callback is satisfied.
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        approval_callback: Optional[Callable[[List[str]], bool]] = None,
    ) -> None:
        """
        Parameters
        ----------
        settings:
            Runtime settings (for limit references).
        approval_callback:
            Optional callable that receives the list of domains and returns
            ``True`` to approve or ``False`` to deny.  If ``None``, approval
            is auto-granted.
        """
        self._settings = settings or Settings()
        self._approval_callback = approval_callback

    def approve(self, domains: List[str]) -> None:
        """Approve or deny swarm creation.

        Raises
        ------
        PermissionError
            If the approval callback returns ``False``.
        ValueError
            If no domains are provided.
        """
        if not domains:
            raise ValueError("Cannot create a swarm with no domains.")

        if len(domains) > self._settings.max_agents_per_swarm:
            raise PermissionError(
                f"Swarm size {len(domains)} exceeds maximum "
                f"of {self._settings.max_agents_per_swarm} agents."
            )

        if self._approval_callback is not None:
            if not self._approval_callback(domains):
                raise PermissionError(
                    f"Swarm creation denied by approval callback for domains: "
                    f"{', '.join(domains)}"
                )
