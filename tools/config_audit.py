"""Configuration audit tool: analyze config files for issues."""

from pyagentspec.property import ListProperty, ObjectProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

audit_config = ServerTool(
    name="audit_config",
    description=(
        "Analyze configuration files for correctness, security issues, "
        "and best-practice violations. Supports common formats: YAML, JSON, "
        "TOML, INI, nginx, Apache, systemd units, Kubernetes manifests, "
        "Terraform HCL, and Dockerfile."
    ),
    inputs=[
        StringProperty(
            title="config_path",
            description="Path to the configuration file or directory to audit",
        ),
        StringProperty(
            title="config_type",
            description="Type of configuration (auto-detected if empty): yaml, json, toml, ini, nginx, k8s, terraform, dockerfile, systemd",
            default="",
        ),
        StringProperty(
            title="check_categories",
            description="Comma-separated categories to check: syntax, security, performance, best_practices, or empty for all",
            default="",
        ),
    ],
    outputs=[
        ListProperty(
            title="findings",
            description="List of audit findings",
            item_type=ObjectProperty(
                title="finding",
                properties={
                    "severity": StringProperty(title="severity"),
                    "category": StringProperty(title="category"),
                    "location": StringProperty(title="location"),
                    "message": StringProperty(title="message"),
                    "recommendation": StringProperty(title="recommendation"),
                },
            ),
        ),
        StringProperty(
            title="summary",
            description="Overall audit summary and risk assessment",
        ),
    ],
    requires_confirmation=False,
)
