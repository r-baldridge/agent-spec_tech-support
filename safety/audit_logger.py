"""Audit trail SpanProcessor: logs all tool invocations and agent decisions."""

import json
import os
import time
from typing import Optional

from pyagentspec.tracing.events.event import Event
from pyagentspec.tracing.spanprocessor import SpanProcessor
from pyagentspec.tracing.spans.span import Span

from config.settings import Settings


class AuditSpanProcessor(SpanProcessor):
    """Custom SpanProcessor that writes an audit trail to a JSON-lines file.

    Each span start/end and event is logged with timestamp, span name,
    and relevant attributes for post-hoc auditing.
    """

    def __init__(
        self,
        settings: Optional[Settings] = None,
        mask_sensitive_information: bool = True,
    ) -> None:
        super().__init__(mask_sensitive_information=mask_sensitive_information)
        self._settings = settings or Settings()
        self._log_dir = self._settings.audit_log_dir
        self._log_file: Optional[str] = None
        self._file_handle = None

    def _ensure_log_file(self) -> None:
        if self._file_handle is None:
            os.makedirs(self._log_dir, exist_ok=True)
            self._log_file = os.path.join(
                self._log_dir, f"audit_{int(time.time())}.jsonl"
            )
            self._file_handle = open(self._log_file, "a", encoding="utf-8")

    def _write_entry(self, entry_type: str, name: str, details: str = "") -> None:
        self._ensure_log_file()
        record = {
            "timestamp": time.time(),
            "type": entry_type,
            "name": name,
            "details": details,
        }
        assert self._file_handle is not None
        self._file_handle.write(json.dumps(record) + "\n")
        self._file_handle.flush()

    # -- Synchronous hooks --

    def on_start(self, span: Span) -> None:
        self._write_entry("span_start", span.name)

    def on_end(self, span: Span) -> None:
        self._write_entry("span_end", span.name)

    def on_event(self, event: Event, span: Span) -> None:
        self._write_entry("event", span.name, str(event.name))

    def startup(self) -> None:
        self._ensure_log_file()

    def shutdown(self) -> None:
        if self._file_handle is not None:
            self._file_handle.close()
            self._file_handle = None

    # -- Asynchronous hooks (delegate to sync versions) --

    async def on_start_async(self, span: Span) -> None:
        self.on_start(span)

    async def on_end_async(self, span: Span) -> None:
        self.on_end(span)

    async def on_event_async(self, event: Event, span: Span) -> None:
        self.on_event(event, span)

    async def startup_async(self) -> None:
        self.startup()

    async def shutdown_async(self) -> None:
        self.shutdown()
