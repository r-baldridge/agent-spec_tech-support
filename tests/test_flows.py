"""Tests for flow construction and FlowBuilder validation."""

import pytest
from pyagentspec.flows.flow import Flow
from pyagentspec.serialization import AgentSpecSerializer

from agents.specialist_registry import SpecialistRegistry
from modes.specialist_workflow_mode import build_specialist_workflow
from modes.expert_review_mode import build_expert_review_flow
from modes.orchestrator import build_orchestrator
from modes.manager_mode import build_manager_workers
from flows.diagnostic_flow import build_diagnostic_flow
from flows.incident_response_flow import build_incident_response_flow
from flows.change_validation_flow import build_change_validation_flow


class TestSpecialistWorkflow:
    def test_build_specialist_workflow(self, base_agent, dummy_llm_config):
        specialist = SpecialistRegistry.build("networking", base_agent)
        flow = build_specialist_workflow(specialist, dummy_llm_config)
        assert isinstance(flow, Flow)
        assert flow.name == "specialist_diagnostic_workflow"

    def test_specialist_workflow_has_correct_nodes(self, base_agent, dummy_llm_config):
        specialist = SpecialistRegistry.build("database", base_agent)
        flow = build_specialist_workflow(specialist, dummy_llm_config)
        node_names = {n.name for n in flow.nodes}
        assert "plan_investigation" in node_names
        assert "collect_evidence" in node_names
        assert "root_cause_analysis" in node_names
        assert "remediate" in node_names


class TestDiagnosticFlow:
    def test_build_diagnostic_flow(self, base_agent, dummy_llm_config):
        specialist = SpecialistRegistry.build("os_linux", base_agent)
        flow = build_diagnostic_flow(specialist, dummy_llm_config)
        assert isinstance(flow, Flow)
        assert flow.name == "diagnostic_flow"


class TestIncidentResponseFlow:
    def test_build_incident_response_flow(self, base_agent, dummy_llm_config):
        specialist = SpecialistRegistry.build("security", base_agent)
        flow = build_incident_response_flow(specialist, dummy_llm_config)
        assert isinstance(flow, Flow)
        node_names = {n.name for n in flow.nodes}
        assert "incident_assessment" in node_names
        assert "incident_containment" in node_names
        assert "incident_remediation" in node_names
        assert "incident_verification" in node_names


class TestChangeValidationFlow:
    def test_build_change_validation_flow(self, base_agent, dummy_llm_config):
        specialist = SpecialistRegistry.build("cloud_infra", base_agent)
        flow = build_change_validation_flow(specialist, dummy_llm_config)
        assert isinstance(flow, Flow)
        node_names = {n.name for n in flow.nodes}
        assert "pre_change_check" in node_names
        assert "apply_change" in node_names
        assert "post_change_check" in node_names
        assert "change_comparison" in node_names


class TestExpertReviewFlow:
    def test_build_expert_review_flow(self, expert_reviewer):
        flow = build_expert_review_flow(expert_reviewer)
        assert isinstance(flow, Flow)
        assert flow.name == "expert_review_flow"


class TestOrchestrator:
    def test_build_orchestrator(self, triage_manager, base_agent, expert_reviewer, dummy_llm_config):
        mw = build_manager_workers(triage_manager, base_agent)
        flow = build_orchestrator(mw, expert_reviewer, dummy_llm_config)
        assert isinstance(flow, Flow)
        assert flow.name == "tech_support_orchestrator"

    def test_orchestrator_has_branching(self, triage_manager, base_agent, expert_reviewer, dummy_llm_config):
        mw = build_manager_workers(triage_manager, base_agent)
        flow = build_orchestrator(mw, expert_reviewer, dummy_llm_config)
        node_names = {n.name for n in flow.nodes}
        assert "escalation_branch" in node_names
        assert "triage_and_investigate" in node_names
        assert "expert_review" in node_names


class TestFlowSerialization:
    def test_specialist_workflow_serializes(self, base_agent, dummy_llm_config):
        specialist = SpecialistRegistry.build("monitoring", base_agent)
        flow = build_specialist_workflow(specialist, dummy_llm_config)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(flow)
        assert "component_type: Flow" in yaml_str

    def test_orchestrator_serializes(self, triage_manager, base_agent, expert_reviewer, dummy_llm_config):
        mw = build_manager_workers(triage_manager, base_agent)
        flow = build_orchestrator(mw, expert_reviewer, dummy_llm_config)
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(flow)
        assert "component_type: Flow" in yaml_str
