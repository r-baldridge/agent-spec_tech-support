"""Resource limiter: enforces concurrent swarm and agent limits."""

import threading
from typing import Optional

from config.settings import Settings


class ResourceLimiter:
    """Enforces concurrency limits on swarm creation and agent counts.

    Thread-safe — safe to use from concurrent orchestrators.
    """

    def __init__(self, settings: Optional[Settings] = None) -> None:
        self._settings = settings or Settings()
        self._lock = threading.Lock()
        self._active_swarms = 0

    @property
    def active_swarms(self) -> int:
        with self._lock:
            return self._active_swarms

    def check_swarm_limits(self, agent_count: int) -> None:
        """Check whether a new swarm can be created.

        Raises
        ------
        ResourceWarning
            If the concurrent swarm limit would be exceeded.
        ValueError
            If the agent count exceeds the per-swarm limit.
        """
        if agent_count > self._settings.max_agents_per_swarm:
            raise ValueError(
                f"Requested {agent_count} agents exceeds per-swarm limit "
                f"of {self._settings.max_agents_per_swarm}."
            )

        with self._lock:
            if self._active_swarms >= self._settings.max_concurrent_swarms:
                raise ResourceWarning(
                    f"Concurrent swarm limit reached "
                    f"({self._settings.max_concurrent_swarms}). "
                    f"Wait for an active swarm to complete."
                )

    def acquire_swarm(self) -> None:
        """Register a new active swarm.  Call when a swarm starts."""
        with self._lock:
            if self._active_swarms >= self._settings.max_concurrent_swarms:
                raise ResourceWarning(
                    f"Cannot acquire: concurrent swarm limit reached "
                    f"({self._settings.max_concurrent_swarms})."
                )
            self._active_swarms += 1

    def release_swarm(self) -> None:
        """Deregister an active swarm.  Call when a swarm completes."""
        with self._lock:
            self._active_swarms = max(0, self._active_swarms - 1)
