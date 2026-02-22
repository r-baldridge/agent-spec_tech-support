"""Tests for round-trip serialization of all major components."""

import yaml
import pytest
from pyagentspec.serialization import AgentSpecSerializer

from agents.specialist_registry import SpecialistRegistry
from modes.manager_mode import build_manager_workers
from modes.orchestrator import build_orchestrator
from modes.swarm_mode import build_swarm
from tools.tool_registry import ToolRegistry


class TestToolSerialization:
    """Verify all tools round-trip through YAML serialization."""

    @pytest.mark.parametrize("tool_name", list(ToolRegistry.all_tools().keys()))
    def test_tool_yaml_round_trip(self, tool_name):
        tool = ToolRegistry.get(tool_name)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(tool)

        # Parse back to dict and verify structure
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "ServerTool"
        assert data["name"] == tool_name

    @pytest.mark.parametrize("tool_name", list(ToolRegistry.all_tools().keys()))
    def test_tool_json_round_trip(self, tool_name):
        import json
        tool = ToolRegistry.get(tool_name)
        serializer = AgentSpecSerializer()
        json_str = serializer.to_json(tool)
        data = json.loads(json_str)
        assert data["component_type"] == "ServerTool"
        assert data["name"] == tool_name


class TestAgentSerialization:
    """Verify agents round-trip through YAML."""

    def test_base_agent_yaml_round_trip(self, base_agent):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(base_agent)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "Agent"
        assert data["name"] == "tech_support_base_agent"

    @pytest.mark.parametrize("domain", SpecialistRegistry.domains())
    def test_specialist_yaml_round_trip(self, base_agent, domain):
        specialist = SpecialistRegistry.build(domain, base_agent)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(specialist)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "SpecializedAgent"

    def test_triage_manager_yaml_round_trip(self, triage_manager):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(triage_manager)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "Agent"
        assert data["name"] == "triage_manager"

    def test_expert_reviewer_yaml_round_trip(self, expert_reviewer):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(expert_reviewer)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "Agent"
        assert data["name"] == "expert_reviewer"


class TestModeSerialization:
    """Verify mode assemblies round-trip through YAML."""

    def test_manager_workers_yaml_round_trip(self, triage_manager, base_agent):
        mw = build_manager_workers(triage_manager, base_agent)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(mw)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "ManagerWorkers"

    def test_swarm_yaml_round_trip(self, base_agent):
        swarm = build_swarm("networking", ["security"], base_agent)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(swarm)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "Swarm"

    def test_orchestrator_yaml_round_trip(self, triage_manager, base_agent, expert_reviewer, dummy_llm_config):
        mw = build_manager_workers(triage_manager, base_agent)
        flow = build_orchestrator(mw, expert_reviewer, dummy_llm_config)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(flow)
        data = yaml.safe_load(yaml_str)
        assert data["component_type"] == "Flow"
        assert data["name"] == "tech_support_orchestrator"
