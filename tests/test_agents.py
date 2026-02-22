"""Tests for agent construction and property inference."""

import pytest
from pyagentspec.agent import Agent
from pyagentspec.specialized_agent import SpecializedAgent
from pyagentspec.serialization import AgentSpecSerializer

from agents.specialist_registry import SpecialistRegistry


class TestBaseAgent:
    def test_base_agent_is_agent(self, base_agent):
        assert isinstance(base_agent, Agent)

    def test_base_agent_has_tools(self, base_agent):
        assert len(base_agent.tools) == 7

    def test_base_agent_human_in_the_loop(self, base_agent):
        assert base_agent.human_in_the_loop is True

    def test_base_agent_has_system_prompt(self, base_agent):
        assert "Diagnostic Methodology" in base_agent.system_prompt


class TestSpecialists:
    @pytest.mark.parametrize("domain", SpecialistRegistry.domains())
    def test_specialist_construction(self, base_agent, domain):
        specialist = SpecialistRegistry.build(domain, base_agent)
        assert isinstance(specialist, SpecializedAgent)
        assert specialist.agent is base_agent

    @pytest.mark.parametrize("domain", SpecialistRegistry.domains())
    def test_specialist_has_additional_instructions(self, base_agent, domain):
        specialist = SpecialistRegistry.build(domain, base_agent)
        params = specialist.agent_specialization_parameters
        assert params.additional_instructions is not None
        assert len(params.additional_instructions) > 100

    @pytest.mark.parametrize("domain", SpecialistRegistry.domains())
    def test_specialist_has_additional_tools(self, base_agent, domain):
        specialist = SpecialistRegistry.build(domain, base_agent)
        params = specialist.agent_specialization_parameters
        assert params.additional_tools is not None
        assert len(params.additional_tools) >= 1

    def test_build_all_returns_8_specialists(self, base_agent):
        all_specialists = SpecialistRegistry.build_all(base_agent)
        assert len(all_specialists) == 8

    def test_build_unknown_domain_raises(self, base_agent):
        with pytest.raises(KeyError):
            SpecialistRegistry.build("quantum_computing", base_agent)


class TestTriageManager:
    def test_triage_manager_is_agent(self, triage_manager):
        assert isinstance(triage_manager, Agent)

    def test_triage_manager_has_ticket_tools(self, triage_manager):
        tool_names = {t.name for t in triage_manager.tools}
        assert "create_ticket" in tool_names
        assert "update_ticket" in tool_names
        assert "query_tickets" in tool_names

    def test_triage_manager_has_knowledge_tools(self, triage_manager):
        tool_names = {t.name for t in triage_manager.tools}
        assert "knowledge_search" in tool_names
        assert "check_alerts" in tool_names


class TestExpertReviewer:
    def test_expert_reviewer_is_agent(self, expert_reviewer):
        assert isinstance(expert_reviewer, Agent)

    def test_expert_reviewer_has_read_only_tools(self, expert_reviewer):
        tool_names = {t.name for t in expert_reviewer.tools}
        assert "shell_read_only" in tool_names
        assert "audit_config" in tool_names
        assert "query_metrics" in tool_names

    def test_expert_reviewer_no_shell_execute(self, expert_reviewer):
        tool_names = {t.name for t in expert_reviewer.tools}
        assert "shell_execute" not in tool_names


class TestAgentSerialization:
    def test_base_agent_serializes(self, base_agent):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(base_agent)
        assert "component_type: Agent" in yaml_str

    @pytest.mark.parametrize("domain", SpecialistRegistry.domains())
    def test_specialist_serializes(self, base_agent, domain):
        specialist = SpecialistRegistry.build(domain, base_agent)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(specialist)
        assert "component_type: SpecializedAgent" in yaml_str

    def test_triage_manager_serializes(self, triage_manager):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(triage_manager)
        assert "triage_manager" in yaml_str

    def test_expert_reviewer_serializes(self, expert_reviewer):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(expert_reviewer)
        assert "expert_reviewer" in yaml_str
