"""Safety policy configuration: command allowlists and RBAC rules."""

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class SafetyPolicy:
    """Declarative command-safety policy for shell execution tools."""

    # Commands that are always safe (no confirmation needed)
    read_only_commands: FrozenSet[str] = field(default_factory=lambda: frozenset({
        "cat", "head", "tail", "less", "more", "grep", "awk", "sed",
        "find", "ls", "ll", "dir", "stat", "file", "wc",
        "df", "du", "free", "uptime", "uname", "hostname", "whoami",
        "id", "groups", "env", "printenv", "date", "cal",
        "ps", "top", "htop", "vmstat", "iostat", "mpstat", "sar",
        "netstat", "ss", "ip", "ifconfig", "route", "arp",
        "dig", "nslookup", "host", "whois",
        "ping", "traceroute", "tracepath", "mtr",
        "curl", "wget",
        "journalctl", "dmesg", "last", "lastlog", "who", "w",
        "systemctl status", "systemctl is-active", "systemctl is-enabled",
        "docker ps", "docker logs", "docker inspect", "docker stats",
        "kubectl get", "kubectl describe", "kubectl logs", "kubectl top",
        "git status", "git log", "git diff", "git show", "git branch",
        "openssl s_client", "openssl x509",
        "mysql -e", "psql -c", "redis-cli info", "redis-cli ping",
    }))

    # Commands that require explicit human confirmation
    destructive_commands: FrozenSet[str] = field(default_factory=lambda: frozenset({
        "rm", "rmdir", "mv", "cp",
        "systemctl start", "systemctl stop", "systemctl restart", "systemctl reload",
        "docker stop", "docker rm", "docker restart",
        "kubectl delete", "kubectl apply", "kubectl rollout",
        "iptables", "firewall-cmd",
        "useradd", "userdel", "usermod", "passwd",
        "chmod", "chown", "chgrp",
        "mount", "umount",
        "apt", "yum", "dnf", "pip install",
        "terraform apply", "terraform destroy",
        "ansible-playbook",
    }))

    # Commands that are absolutely blocked (never executed)
    blocked_commands: FrozenSet[str] = field(default_factory=lambda: frozenset({
        "rm -rf /",
        "rm -rf /*",
        "mkfs",
        "dd if=/dev/zero",
        ":(){ :|:& };:",
        "chmod -R 777 /",
        "shutdown", "reboot", "halt", "poweroff", "init 0", "init 6",
        "> /dev/sda",
        "mv / /dev/null",
    }))

    def classify_command(self, command: str) -> str:
        """Classify a command as 'safe', 'confirm', or 'blocked'.

        Returns
        -------
        str
            One of ``"safe"``, ``"confirm"``, or ``"blocked"``.
        """
        stripped = command.strip()

        for blocked in self.blocked_commands:
            if stripped == blocked or stripped.startswith(blocked + " "):
                return "blocked"

        for destructive in self.destructive_commands:
            if stripped.startswith(destructive):
                return "confirm"

        for safe in self.read_only_commands:
            if stripped.startswith(safe):
                return "safe"

        # Unknown commands default to requiring confirmation
        return "confirm"
