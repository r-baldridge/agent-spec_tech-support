"""Monitoring and metrics tools: query time-series metrics and check alerts."""

from pyagentspec.property import ListProperty, ObjectProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

query_metrics = ServerTool(
    name="query_metrics",
    description=(
        "Query time-series metrics from monitoring systems (Prometheus, "
        "CloudWatch, Datadog, etc.). Supports PromQL and provider-specific "
        "query languages. Returns metric values with timestamps."
    ),
    inputs=[
        StringProperty(
            title="query",
            description="Metric query (e.g., PromQL expression like 'rate(http_requests_total[5m])')",
        ),
        StringProperty(
            title="time_range",
            description="Time range for the query (e.g., '1h', '6h', '24h', '7d')",
            default="1h",
        ),
        StringProperty(
            title="step",
            description="Resolution step for range queries (e.g., '15s', '1m', '5m')",
            default="1m",
        ),
    ],
    outputs=[
        ListProperty(
            title="series",
            description="List of metric time series",
            item_type=ObjectProperty(
                title="metric_series",
                properties={
                    "labels": StringProperty(title="labels"),
                    "values": StringProperty(title="values"),
                },
            ),
        ),
        StringProperty(
            title="summary",
            description="Human-readable summary of the metric data",
        ),
    ],
    requires_confirmation=False,
)

check_alerts = ServerTool(
    name="check_alerts",
    description=(
        "Check the current state of alerts from monitoring and alerting "
        "systems. Returns active, firing, and recently resolved alerts "
        "with their severity and affected components."
    ),
    inputs=[
        StringProperty(
            title="filter",
            description="Optional filter expression for alerts (e.g., service name, severity)",
            default="",
        ),
        StringProperty(
            title="state",
            description="Alert state filter: 'firing', 'pending', 'resolved', or empty for all",
            default="firing",
        ),
    ],
    outputs=[
        ListProperty(
            title="alerts",
            description="List of matching alerts",
            item_type=ObjectProperty(
                title="alert",
                properties={
                    "alert_name": StringProperty(title="alert_name"),
                    "severity": StringProperty(title="severity"),
                    "state": StringProperty(title="state"),
                    "description": StringProperty(title="description"),
                    "started_at": StringProperty(title="started_at"),
                    "labels": StringProperty(title="labels"),
                },
            ),
        ),
    ],
    requires_confirmation=False,
)
