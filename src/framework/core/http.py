"""A `requests.Session` wrapper used by every API client: a base URL, a timeout on every call,
a correlation ID on every request, logging, and a redacted transcript of every call for the
test's evidence (`transcript.json` and `transcript.md`). Tests never use `requests` directly.
"""

import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from framework.core.redaction import redact_headers, redact_json, redact_text

LOG = logging.getLogger(__name__)
CORRELATION_HEADER = "X-Correlation-ID"
_MAX_BODY = 20_000


@dataclass(frozen=True)
class Call:
    """One request and its response (or the error), already redacted."""

    target: str
    method: str
    url: str
    request_headers: dict[str, str]
    request_body: Any
    status: int | None
    response_headers: dict[str, str]
    response_body: Any
    duration_ms: float
    correlation_id: str
    started_at: str
    error: str | None = None


@dataclass
class Transcript:
    """Every call one test made, in order."""

    calls: list[Call] = field(default_factory=list)

    def add(self, call: Call) -> None:
        self.calls.append(call)

    def write(self, directory: Path) -> list[str]:
        """Writes transcript.json and transcript.md; returns the file names written."""
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "transcript.json").write_text(
            json.dumps([asdict(c) for c in self.calls], indent=2), encoding="utf-8"
        )
        (directory / "transcript.md").write_text(self.markdown(), encoding="utf-8")
        return ["transcript.json", "transcript.md"]

    def markdown(self) -> str:
        lines = ["# API transcript", ""]
        if not self.calls:
            lines.append("(no calls)")
        for number, call in enumerate(self.calls, start=1):
            outcome = call.error or f"{call.status}"
            lines += [
                f"## {number}. {call.method} {call.url} → {outcome} ({call.duration_ms:.0f} ms)",
                "",
                (
                    f"Target `{call.target}`, correlation ID `{call.correlation_id}`, "
                    f"at {call.started_at}"
                ),
                "",
            ]
            if call.request_body is not None:
                lines += ["Request body:", "", "```json", _pretty(call.request_body), "```", ""]
            if call.response_body is not None:
                lines += ["Response body:", "", "```json", _pretty(call.response_body), "```", ""]
        return "\n".join(lines) + "\n"


def _pretty(body: Any) -> str:
    return json.dumps(body, indent=2) if not isinstance(body, str) else body


def _body(content: bytes | str | None, content_type: str) -> Any:
    if not content:
        return None
    text = content.decode("utf-8", errors="replace") if isinstance(content, bytes) else content
    if "json" in content_type:
        try:
            return redact_json(json.loads(text))
        except json.JSONDecodeError:
            pass
    return redact_text(text[:_MAX_BODY])


class ApiSession:
    """One target's HTTP session. Each call is logged and added to the current transcript."""

    def __init__(
        self,
        target: str,
        base_url: str,
        timeout: tuple[float, float],
        transcript: Transcript | None = None,
        default_headers: dict[str, str] | None = None,
    ) -> None:
        self.target = target
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transcript = transcript
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})
        self._session.headers.update(default_headers or {})

    def close(self) -> None:
        self._session.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        headers: dict[str, str] | None = None,
        timeout: tuple[float, float] | None = None,
    ) -> requests.Response:
        correlation_id = str(uuid.uuid4())
        request_headers = {CORRELATION_HEADER: correlation_id, **(headers or {})}
        url = f"{self.base_url}{path}"
        started = datetime.now(UTC).isoformat()
        clock = time.perf_counter()
        try:
            response = self._session.request(
                method,
                url,
                json=json_body,
                headers=request_headers,
                timeout=timeout or self.timeout,
            )
        except requests.RequestException as error:
            self._record(method, url, request_headers, json_body, None, started, clock, error)
            raise
        self._record(method, url, request_headers, json_body, response, started, clock, None)
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", path, **kwargs)

    def _record(
        self,
        method: str,
        url: str,
        headers: dict[str, str],
        body: Any,
        response: requests.Response | None,
        started: str,
        clock: float,
        error: Exception | None,
    ) -> None:
        duration_ms = (time.perf_counter() - clock) * 1000
        sent = {**{k: str(v) for k, v in self._session.headers.items()}, **headers}
        call = Call(
            target=self.target,
            method=method,
            url=redact_text(url),
            request_headers=redact_headers(sent),
            request_body=redact_json(body) if body is not None else None,
            status=response.status_code if response is not None else None,
            response_headers=redact_headers(dict(response.headers)) if response is not None else {},
            response_body=(
                _body(response.content, response.headers.get("Content-Type", ""))
                if response is not None
                else None
            ),
            duration_ms=round(duration_ms, 1),
            correlation_id=headers[CORRELATION_HEADER],
            started_at=started,
            error=f"{type(error).__name__}: {error}" if error else None,
        )
        LOG.info(
            "%s %s %s -> %s (%.0f ms)",
            self.target,
            method,
            call.url,
            call.status if error is None else call.error,
            duration_ms,
        )
        if self.transcript is not None:
            self.transcript.add(call)
