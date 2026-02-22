"""Shell execution tools: confirmed (write) and read-only (safe)."""

from pyagentspec.property import IntegerProperty, StringProperty
from pyagentspec.tools.servertool import ServerTool

shell_execute = ServerTool(
    name="shell_execute",
    description=(
        "Execute a shell command on the target system. "
        "Write operations require human approval before execution. "
        "Use this tool when you need to make changes to the system, "
        "install packages, restart services, or modify files."
    ),
    inputs=[
        StringProperty(
            title="command",
            description="The shell command to execute",
        ),
        StringProperty(
            title="working_directory",
            description="Working directory for command execution",
            default="/tmp",
        ),
        IntegerProperty(
            title="timeout_seconds",
            description="Maximum execution time in seconds",
            default=60,
        ),
    ],
    outputs=[
        StringProperty(
            title="stdout",
            description="Standard output from the command",
        ),
        StringProperty(
            title="stderr",
            description="Standard error from the command",
        ),
        IntegerProperty(
            title="exit_code",
            description="Exit code of the command (0 = success)",
        ),
    ],
    requires_confirmation=True,
)

shell_read_only = ServerTool(
    name="shell_read_only",
    description=(
        "Execute a read-only shell command on the target system. "
        "Limited to safe, non-destructive commands such as viewing files, "
        "checking system status, listing processes, and reading logs. "
        "No human approval is required."
    ),
    inputs=[
        StringProperty(
            title="command",
            description="The read-only shell command to execute",
        ),
        StringProperty(
            title="working_directory",
            description="Working directory for command execution",
            default="/tmp",
        ),
        IntegerProperty(
            title="timeout_seconds",
            description="Maximum execution time in seconds",
            default=30,
        ),
    ],
    outputs=[
        StringProperty(
            title="stdout",
            description="Standard output from the command",
        ),
        StringProperty(
            title="stderr",
            description="Standard error from the command",
        ),
        IntegerProperty(
            title="exit_code",
            description="Exit code of the command (0 = success)",
        ),
    ],
    requires_confirmation=False,
)
