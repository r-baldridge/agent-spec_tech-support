"""Resource monitoring tool: CPU, memory, disk, processes, sockets."""

from pyagentspec.property import ListProperty, ObjectProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

resource_monitor = ServerTool(
    name="resource_monitor",
    description=(
        "Monitor system resource utilization including CPU, memory, disk, "
        "running processes, and network sockets. Provides a real-time snapshot "
        "of the target system's health and resource consumption."
    ),
    inputs=[
        StringProperty(
            title="target_host",
            description="Hostname or IP to monitor (use 'localhost' for local system)",
            default="localhost",
        ),
        StringProperty(
            title="resource_type",
            description="Resource to monitor: cpu, memory, disk, processes, sockets, or 'all' for a full report",
            default="all",
        ),
        StringProperty(
            title="sort_by",
            description="Sort criteria for process listing: cpu, memory, pid, name",
            default="cpu",
        ),
    ],
    outputs=[
        ObjectProperty(
            title="system_info",
            description="System identification and uptime",
            properties={
                "hostname": StringProperty(title="hostname"),
                "uptime": StringProperty(title="uptime"),
                "kernel": StringProperty(title="kernel"),
            },
        ),
        StringProperty(
            title="cpu_usage",
            description="CPU utilization summary",
        ),
        StringProperty(
            title="memory_usage",
            description="Memory utilization summary",
        ),
        StringProperty(
            title="disk_usage",
            description="Disk utilization summary",
        ),
        ListProperty(
            title="top_processes",
            description="Top resource-consuming processes",
            item_type=ObjectProperty(
                title="process",
                properties={
                    "pid": StringProperty(title="pid"),
                    "name": StringProperty(title="name"),
                    "cpu_percent": StringProperty(title="cpu_percent"),
                    "memory_percent": StringProperty(title="memory_percent"),
                },
            ),
        ),
        ListProperty(
            title="listening_sockets",
            description="Active listening network sockets",
            item_type=ObjectProperty(
                title="socket",
                properties={
                    "protocol": StringProperty(title="protocol"),
                    "address": StringProperty(title="address"),
                    "port": StringProperty(title="port"),
                    "process": StringProperty(title="process"),
                },
            ),
        ),
    ],
    requires_confirmation=False,
)
