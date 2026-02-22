"""Tests for safety modules: allowlist, approval gate, resource limiter, audit."""

import os
import tempfile
import time

import pytest

from config.safety_policy import SafetyPolicy
from config.settings import Settings
from safety.command_allowlist import CommandAllowlist
from safety.approval_gate import SwarmApprovalGate
from safety.resource_limiter import ResourceLimiter
from safety.audit_logger import AuditSpanProcessor


class TestSafetyPolicy:
    def test_read_only_command_is_safe(self):
        policy = SafetyPolicy()
        assert policy.classify_command("cat /etc/hosts") == "safe"

    def test_destructive_command_needs_confirm(self):
        policy = SafetyPolicy()
        assert policy.classify_command("rm file.txt") == "confirm"

    def test_blocked_command(self):
        policy = SafetyPolicy()
        assert policy.classify_command("rm -rf /") == "blocked"

    def test_unknown_command_needs_confirm(self):
        policy = SafetyPolicy()
        assert policy.classify_command("some_unknown_command") == "confirm"

    def test_systemctl_status_is_safe(self):
        policy = SafetyPolicy()
        assert policy.classify_command("systemctl status nginx") == "safe"

    def test_systemctl_restart_needs_confirm(self):
        policy = SafetyPolicy()
        assert policy.classify_command("systemctl restart nginx") == "confirm"


class TestCommandAllowlist:
    def test_is_safe(self):
        al = CommandAllowlist()
        assert al.is_safe("ls -la /tmp")
        assert not al.is_safe("rm file.txt")

    def test_needs_confirmation(self):
        al = CommandAllowlist()
        assert al.needs_confirmation("rm file.txt")
        assert not al.needs_confirmation("ls /tmp")

    def test_is_blocked(self):
        al = CommandAllowlist()
        assert al.is_blocked("rm -rf /")
        assert not al.is_blocked("ls /tmp")

    def test_validate_raises_on_blocked(self):
        al = CommandAllowlist()
        with pytest.raises(PermissionError):
            al.validate("rm -rf /")

    def test_validate_returns_classification(self):
        al = CommandAllowlist()
        assert al.validate("ls /tmp") == "safe"
        assert al.validate("rm file.txt") == "confirm"


class TestSwarmApprovalGate:
    def test_approve_with_no_callback(self):
        gate = SwarmApprovalGate()
        gate.approve(["networking", "security"])  # Should not raise

    def test_approve_empty_domains_raises(self):
        gate = SwarmApprovalGate()
        with pytest.raises(ValueError):
            gate.approve([])

    def test_approve_exceeds_limit_raises(self):
        settings = Settings()
        settings.max_agents_per_swarm = 2
        gate = SwarmApprovalGate(settings=settings)
        with pytest.raises(PermissionError):
            gate.approve(["a", "b", "c"])

    def test_approve_callback_deny(self):
        gate = SwarmApprovalGate(approval_callback=lambda d: False)
        with pytest.raises(PermissionError):
            gate.approve(["networking"])

    def test_approve_callback_allow(self):
        gate = SwarmApprovalGate(approval_callback=lambda d: True)
        gate.approve(["networking"])  # Should not raise


class TestResourceLimiter:
    def test_initial_active_swarms_is_zero(self):
        limiter = ResourceLimiter()
        assert limiter.active_swarms == 0

    def test_acquire_and_release(self):
        limiter = ResourceLimiter()
        limiter.acquire_swarm()
        assert limiter.active_swarms == 1
        limiter.release_swarm()
        assert limiter.active_swarms == 0

    def test_exceeds_concurrent_limit(self):
        settings = Settings()
        settings.max_concurrent_swarms = 1
        limiter = ResourceLimiter(settings=settings)
        limiter.acquire_swarm()
        with pytest.raises(ResourceWarning):
            limiter.acquire_swarm()
        limiter.release_swarm()

    def test_exceeds_agent_limit(self):
        settings = Settings()
        settings.max_agents_per_swarm = 3
        limiter = ResourceLimiter(settings=settings)
        with pytest.raises(ValueError):
            limiter.check_swarm_limits(agent_count=5)

    def test_release_never_goes_negative(self):
        limiter = ResourceLimiter()
        limiter.release_swarm()
        assert limiter.active_swarms == 0


class TestAuditSpanProcessor:
    def test_startup_creates_log_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings = Settings()
            settings.audit_log_dir = tmpdir
            processor = AuditSpanProcessor(settings=settings)
            processor.startup()
            assert processor._log_file is not None
            assert os.path.exists(processor._log_file)
            processor.shutdown()

    def test_shutdown_closes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            settings = Settings()
            settings.audit_log_dir = tmpdir
            processor = AuditSpanProcessor(settings=settings)
            processor.startup()
            processor.shutdown()
            assert processor._file_handle is None
