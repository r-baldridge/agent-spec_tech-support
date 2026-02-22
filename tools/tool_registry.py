"""Central registry: tool name -> ServerTool definition lookup."""

from typing import Dict, List

from pyagentspec.tools.servertool import ServerTool

from tools.shell_execution import shell_execute, shell_read_only
from tools.knowledge_retrieval import knowledge_search, incident_history_search
from tools.ticket_management import create_ticket, update_ticket, query_tickets
from tools.monitoring_metrics import query_metrics, check_alerts
from tools.log_analysis import search_logs
from tools.config_audit import audit_config
from tools.network_diagnostic import network_diagnostic
from tools.resource_monitor import resource_monitor


class ToolRegistry:
    """Central registry mapping tool names to their ``ServerTool`` definitions."""

    _tools: Dict[str, ServerTool] = {
        "shell_execute": shell_execute,
        "shell_read_only": shell_read_only,
        "knowledge_search": knowledge_search,
        "incident_history_search": incident_history_search,
        "create_ticket": create_ticket,
        "update_ticket": update_ticket,
        "query_tickets": query_tickets,
        "query_metrics": query_metrics,
        "check_alerts": check_alerts,
        "search_logs": search_logs,
        "audit_config": audit_config,
        "network_diagnostic": network_diagnostic,
        "resource_monitor": resource_monitor,
    }

    @classmethod
    def get(cls, name: str) -> ServerTool:
        """Look up a tool by name. Raises ``KeyError`` if not found."""
        return cls._tools[name]

    @classmethod
    def get_many(cls, *names: str) -> List[ServerTool]:
        """Look up multiple tools by name."""
        return [cls._tools[n] for n in names]

    @classmethod
    def all_tools(cls) -> Dict[str, ServerTool]:
        """Return a copy of the full registry."""
        return dict(cls._tools)

    @classmethod
    def all_tool_objects(cls) -> List[ServerTool]:
        """Return all tool definitions as a list."""
        return list(cls._tools.values())
