"""Knowledge retrieval tools: search documentation and past incidents."""

from pyagentspec.property import IntegerProperty, ListProperty, ObjectProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

knowledge_search = ServerTool(
    name="knowledge_search",
    description=(
        "Search the knowledge base for documentation, runbooks, "
        "troubleshooting guides, and architectural documents. "
        "Returns relevant snippets ranked by relevance."
    ),
    inputs=[
        StringProperty(
            title="query",
            description="Natural-language search query",
        ),
        StringProperty(
            title="domain",
            description="Optional domain filter (e.g., 'networking', 'database', 'security')",
            default="",
        ),
        IntegerProperty(
            title="max_results",
            description="Maximum number of results to return",
            default=5,
        ),
    ],
    outputs=[
        ListProperty(
            title="results",
            description="List of matching knowledge base entries",
            item_type=ObjectProperty(
                title="entry",
                properties={
                    "title": StringProperty(title="title"),
                    "content": StringProperty(title="content"),
                    "source": StringProperty(title="source"),
                    "relevance_score": StringProperty(title="relevance_score"),
                },
            ),
        ),
    ],
    requires_confirmation=False,
)

incident_history_search = ServerTool(
    name="incident_history_search",
    description=(
        "Search past incident records for similar issues, including "
        "root causes, resolutions, and post-mortem notes. "
        "Useful for identifying recurring problems and known solutions."
    ),
    inputs=[
        StringProperty(
            title="query",
            description="Description of the current issue to find similar past incidents",
        ),
        StringProperty(
            title="severity_filter",
            description="Filter by severity level (P1, P2, P3, P4, or empty for all)",
            default="",
        ),
        IntegerProperty(
            title="max_results",
            description="Maximum number of past incidents to return",
            default=5,
        ),
    ],
    outputs=[
        ListProperty(
            title="incidents",
            description="List of similar past incidents",
            item_type=ObjectProperty(
                title="incident",
                properties={
                    "incident_id": StringProperty(title="incident_id"),
                    "title": StringProperty(title="title"),
                    "root_cause": StringProperty(title="root_cause"),
                    "resolution": StringProperty(title="resolution"),
                    "severity": StringProperty(title="severity"),
                    "date": StringProperty(title="date"),
                },
            ),
        ),
    ],
    requires_confirmation=False,
)
