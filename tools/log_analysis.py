"""Log analysis tool: search and filter log entries."""

from pyagentspec.property import IntegerProperty, ListProperty, ObjectProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

search_logs = ServerTool(
    name="search_logs",
    description=(
        "Search logs across centralized logging systems (ELK, Loki, "
        "CloudWatch Logs, etc.). Supports keyword search, regex patterns, "
        "and structured log queries. Returns matching log entries with context."
    ),
    inputs=[
        StringProperty(
            title="query",
            description="Log search query (keywords, regex, or provider-specific query syntax)",
        ),
        StringProperty(
            title="source",
            description="Log source filter (e.g., service name, hostname, container ID)",
            default="",
        ),
        StringProperty(
            title="time_range",
            description="Time range to search (e.g., '15m', '1h', '24h')",
            default="1h",
        ),
        StringProperty(
            title="level",
            description="Minimum log level filter: DEBUG, INFO, WARN, ERROR, FATAL, or empty for all",
            default="",
        ),
        IntegerProperty(
            title="max_results",
            description="Maximum number of log entries to return",
            default=100,
        ),
    ],
    outputs=[
        ListProperty(
            title="entries",
            description="List of matching log entries",
            item_type=ObjectProperty(
                title="log_entry",
                properties={
                    "timestamp": StringProperty(title="timestamp"),
                    "level": StringProperty(title="level"),
                    "source": StringProperty(title="source"),
                    "message": StringProperty(title="message"),
                },
            ),
        ),
        IntegerProperty(
            title="total_matches",
            description="Total number of matching entries (may exceed max_results)",
        ),
    ],
    requires_confirmation=False,
)
