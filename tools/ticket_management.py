"""Ticket management tools: create, update, and query tickets."""

from pyagentspec.property import IntegerProperty, ListProperty, ObjectProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

create_ticket = ServerTool(
    name="create_ticket",
    description=(
        "Create a new support ticket in the ticketing system. "
        "Records the issue description, severity, affected systems, "
        "and assigns it to the appropriate team."
    ),
    inputs=[
        StringProperty(
            title="title",
            description="Concise title for the ticket",
        ),
        StringProperty(
            title="description",
            description="Detailed description of the issue",
        ),
        StringProperty(
            title="severity",
            description="Severity level: P1 (critical), P2 (high), P3 (medium), P4 (low)",
        ),
        StringProperty(
            title="domain",
            description="Technical domain (networking, database, os_linux, cloud_infra, application_code, security, cicd, monitoring)",
        ),
        StringProperty(
            title="affected_systems",
            description="Comma-separated list of affected systems or services",
            default="",
        ),
    ],
    outputs=[
        StringProperty(
            title="ticket_id",
            description="Unique identifier of the newly created ticket",
        ),
        StringProperty(
            title="ticket_url",
            description="URL to view the ticket",
        ),
    ],
    requires_confirmation=True,
)

update_ticket = ServerTool(
    name="update_ticket",
    description=(
        "Add a comment, update status, or change fields on an existing ticket. "
        "Use this to log diagnostic findings, status changes, and resolution notes."
    ),
    inputs=[
        StringProperty(
            title="ticket_id",
            description="Identifier of the ticket to update",
        ),
        StringProperty(
            title="comment",
            description="Comment text to add to the ticket",
            default="",
        ),
        StringProperty(
            title="status",
            description="New status (open, in_progress, pending, resolved, closed), or empty to leave unchanged",
            default="",
        ),
        StringProperty(
            title="assignee",
            description="New assignee, or empty to leave unchanged",
            default="",
        ),
    ],
    outputs=[
        StringProperty(
            title="result",
            description="Confirmation message or error details",
        ),
    ],
    requires_confirmation=False,
)

query_tickets = ServerTool(
    name="query_tickets",
    description=(
        "Search and query existing tickets by various criteria. "
        "Useful for finding related tickets, checking status of known issues, "
        "and understanding the broader context of a problem."
    ),
    inputs=[
        StringProperty(
            title="query",
            description="Search query or ticket ID",
        ),
        StringProperty(
            title="status_filter",
            description="Filter by status (open, in_progress, resolved, closed, or empty for all)",
            default="",
        ),
        IntegerProperty(
            title="max_results",
            description="Maximum number of tickets to return",
            default=10,
        ),
    ],
    outputs=[
        ListProperty(
            title="tickets",
            description="List of matching tickets",
            item_type=ObjectProperty(
                title="ticket",
                properties={
                    "ticket_id": StringProperty(title="ticket_id"),
                    "title": StringProperty(title="title"),
                    "status": StringProperty(title="status"),
                    "severity": StringProperty(title="severity"),
                    "assignee": StringProperty(title="assignee"),
                    "created_at": StringProperty(title="created_at"),
                },
            ),
        ),
    ],
    requires_confirmation=False,
)
