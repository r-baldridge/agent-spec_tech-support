"""Tests for mode assembly: ManagerWorkers, Swarm, mode selection."""

import pytest
from pyagentspec.managerworkers import ManagerWorkers
from pyagentspec.swarm import Swarm, HandoffMode
from pyagentspec.serialization import AgentSpecSerializer

from modes.manager_mode import build_manager_workers
from modes.swarm_mode import build_swarm
from modes.mode_selector import select_mode, OperationalMode
from safety.approval_gate import SwarmApprovalGate
from safety.resource_limiter import ResourceLimiter


class TestManagerMode:
    def test_build_manager_workers(self, triage_manager, base_agent):
        mw = build_manager_workers(triage_manager, base_agent)
        assert isinstance(mw, ManagerWorkers)
        assert mw.group_manager is triage_manager
        assert len(mw.workers) == 8

    def test_manager_workers_serializes(self, triage_manager, base_agent):
        mw = build_manager_workers(triage_manager, base_agent)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(mw)
        assert "component_type: ManagerWorkers" in yaml_str


class TestSwarmMode:
    def test_build_swarm_two_domains(self, base_agent):
        swarm = build_swarm("networking", ["security"], base_agent)
        assert isinstance(swarm, Swarm)
        assert swarm.handoff == HandoffMode.OPTIONAL
        # 2 agents, each can talk to the other: 2 relationships
        assert len(swarm.relationships) == 2

    def test_build_swarm_three_domains(self, base_agent):
        swarm = build_swarm("networking", ["security", "cloud_infra"], base_agent)
        # 3 agents, fully connected: 3 * 2 = 6 relationships
        assert len(swarm.relationships) == 6

    def test_swarm_approval_gate_too_many_agents(self, base_agent):
        from config.settings import Settings
        settings = Settings()
        settings.max_agents_per_swarm = 2
        gate = SwarmApprovalGate(settings=settings)
        with pytest.raises(PermissionError):
            build_swarm(
                "networking",
                ["security", "cloud_infra"],
                base_agent,
                approval_gate=gate,
            )

    def test_swarm_approval_gate_callback_deny(self, base_agent):
        gate = SwarmApprovalGate(approval_callback=lambda domains: False)
        with pytest.raises(PermissionError):
            build_swarm("networking", ["security"], base_agent, approval_gate=gate)

    def test_swarm_serializes(self, base_agent):
        swarm = build_swarm("database", ["monitoring"], base_agent)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(swarm)
        assert "component_type: Swarm" in yaml_str


class TestModeSelector:
    def test_p4_single_domain_returns_manager(self):
        result = select_mode("networking", "P4")
        assert result.mode == OperationalMode.MANAGER

    def test_p1_returns_swarm(self):
        result = select_mode("database", "P1")
        assert result.mode == OperationalMode.SWARM

    def test_cross_domain_returns_swarm(self):
        result = select_mode(
            "networking", "P3",
            cross_domain=True,
            peer_domains=["security", "cloud_infra"],
        )
        assert result.mode == OperationalMode.SWARM

    def test_specialist_resolved_returns_review(self):
        result = select_mode("os_linux", "P3", specialist_resolved=True)
        assert result.mode == OperationalMode.EXPERT_REVIEW
