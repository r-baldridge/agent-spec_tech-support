"""Command allowlist: read-only, destructive, and blocked command sets.

Provides runtime classification of shell commands to enforce the safety policy.
"""

from config.safety_policy import SafetyPolicy


class CommandAllowlist:
    """Wraps a ``SafetyPolicy`` to classify and gate shell commands at runtime."""

    def __init__(self, policy: SafetyPolicy | None = None) -> None:
        self._policy = policy or SafetyPolicy()

    def is_safe(self, command: str) -> bool:
        """Return ``True`` if the command is classified as safe (read-only)."""
        return self._policy.classify_command(command) == "safe"

    def needs_confirmation(self, command: str) -> bool:
        """Return ``True`` if the command requires human confirmation."""
        return self._policy.classify_command(command) == "confirm"

    def is_blocked(self, command: str) -> bool:
        """Return ``True`` if the command is absolutely blocked."""
        return self._policy.classify_command(command) == "blocked"

    def validate(self, command: str) -> str:
        """Validate a command and return its classification.

        Raises
        ------
        PermissionError
            If the command is blocked.
        """
        classification = self._policy.classify_command(command)
        if classification == "blocked":
            raise PermissionError(
                f"Command is blocked by safety policy: {command!r}"
            )
        return classification
