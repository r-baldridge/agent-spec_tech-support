"""Network diagnostic tool: ping, traceroute, DNS, TLS checks, and MTR."""

from pyagentspec.property import StringProperty
from pyagentspec.tools.servertool import ServerTool

network_diagnostic = ServerTool(
    name="network_diagnostic",
    description=(
        "Run network diagnostic tests including ping, traceroute, DNS lookups, "
        "TLS certificate checks, and MTR (My Traceroute). Provides comprehensive "
        "network path and connectivity analysis."
    ),
    inputs=[
        StringProperty(
            title="target",
            description="Target hostname, IP address, or URL to diagnose",
        ),
        StringProperty(
            title="test_type",
            description="Type of diagnostic: ping, traceroute, dns, tls_check, mtr, port_scan",
        ),
        StringProperty(
            title="options",
            description="Additional test-specific options (e.g., DNS record type 'A'/'AAAA'/'MX', port number for port_scan, count for ping)",
            default="",
        ),
    ],
    outputs=[
        StringProperty(
            title="result",
            description="Raw output from the diagnostic test",
        ),
        StringProperty(
            title="analysis",
            description="Structured analysis of the diagnostic results",
        ),
        StringProperty(
            title="status",
            description="Overall status: healthy, degraded, or unreachable",
        ),
    ],
    requires_confirmation=False,
)
