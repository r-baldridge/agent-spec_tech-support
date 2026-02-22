"""Tests for tool definitions: Property schemas and serialization."""

import pytest
from pyagentspec.serialization import AgentSpecSerializer

from tools.tool_registry import ToolRegistry
from tools.shell_execution import shell_execute, shell_read_only
from tools.knowledge_retrieval import knowledge_search, incident_history_search
from tools.ticket_management import create_ticket, update_ticket, query_tickets
from tools.monitoring_metrics import query_metrics, check_alerts
from tools.log_analysis import search_logs
from tools.config_audit import audit_config
from tools.network_diagnostic import network_diagnostic
from tools.resource_monitor import resource_monitor


ALL_TOOLS = [
    shell_execute, shell_read_only,
    knowledge_search, incident_history_search,
    create_ticket, update_ticket, query_tickets,
    query_metrics, check_alerts,
    search_logs,
    audit_config,
    network_diagnostic,
    resource_monitor,
]


class TestToolDefinitions:
    """Validate that all tools are well-formed ServerTool instances."""

    @pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.name)
    def test_tool_has_name_and_description(self, tool):
        assert tool.name
        assert tool.description

    @pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.name)
    def test_tool_has_inputs_and_outputs(self, tool):
        assert tool.inputs is not None and len(tool.inputs) > 0
        assert tool.outputs is not None and len(tool.outputs) > 0

    def test_shell_execute_requires_confirmation(self):
        assert shell_execute.requires_confirmation is True

    def test_shell_read_only_no_confirmation(self):
        assert shell_read_only.requires_confirmation is False

    def test_create_ticket_requires_confirmation(self):
        assert create_ticket.requires_confirmation is True

    def test_update_ticket_no_confirmation(self):
        assert update_ticket.requires_confirmation is False

    @pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.name)
    def test_tool_input_properties_have_titles(self, tool):
        for prop in tool.inputs:
            assert prop.title, f"Input property missing title in {tool.name}"

    @pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.name)
    def test_tool_output_properties_have_titles(self, tool):
        for prop in tool.outputs:
            assert prop.title, f"Output property missing title in {tool.name}"


class TestToolRegistry:
    """Validate ToolRegistry lookup."""

    def test_registry_has_all_tools(self):
        assert len(ToolRegistry.all_tools()) == 13

    def test_registry_get_known_tool(self):
        tool = ToolRegistry.get("shell_execute")
        assert tool.name == "shell_execute"

    def test_registry_get_unknown_raises(self):
        with pytest.raises(KeyError):
            ToolRegistry.get("nonexistent_tool")

    def test_registry_get_many(self):
        tools = ToolRegistry.get_many("shell_execute", "search_logs")
        assert len(tools) == 2
        assert tools[0].name == "shell_execute"
        assert tools[1].name == "search_logs"


class TestToolSerialization:
    """Validate that tools serialize to YAML without errors."""

    @pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.name)
    def test_tool_serializes_to_yaml(self, tool):
        serializer = AgentSpecSerializer()
        yaml_str = serializer.to_yaml(tool)
        assert "component_type: ServerTool" in yaml_str
        assert tool.name in yaml_str

    @pytest.mark.parametrize("tool", ALL_TOOLS, ids=lambda t: t.name)
    def test_tool_serializes_to_json(self, tool):
        serializer = AgentSpecSerializer()
        json_str = serializer.to_json(tool)
        assert '"component_type": "ServerTool"' in json_str
        assert tool.name in json_str
