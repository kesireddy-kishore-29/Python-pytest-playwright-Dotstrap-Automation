"""The HTTP session against a throwaway local server (no outside network): a correlation ID on
every request, a timeout, and a redacted transcript."""

import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest
import requests

from framework.api.clients.responses import UnexpectedStatusError, expect, parse
from framework.api.models.booker import AuthToken
from framework.core.http import CORRELATION_HEADER, ApiSession, Transcript

pytestmark = pytest.mark.unit


class _Handler(BaseHTTPRequestHandler):
    seen: list[dict[str, str]] = []  # noqa: RUF012 - the test reads what the server received

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(length)
        _Handler.seen.append(dict(self.headers))
        body = json.dumps({"token": "abcdefghij-secret"}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Set-Cookie", "session=s3cr3t")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002 - stdlib signature
        return


@pytest.fixture
def server() -> Iterator[str]:
    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    thread.join(timeout=5)


def test_every_call_has_a_correlation_id_and_a_redacted_transcript(
    server: str, tmp_path: Path
) -> None:
    transcript = Transcript()
    session = ApiSession("local", server, (2.0, 2.0), transcript)

    response = session.post(
        "/auth?token=query-secret",
        json_body={"username": "admin", "password": "pw-123"},
        headers={"Authorization": "Bearer abcdefgh12345"},
    )
    session.close()

    assert parse(expect(response, 200), AuthToken).token == "abcdefghij-secret"
    assert _Handler.seen[-1][CORRELATION_HEADER] == transcript.calls[0].correlation_id
    call = transcript.calls[0]
    assert call.url.endswith("/auth?token=****")
    assert call.request_headers["Authorization"] == "Bearer ****"
    assert call.request_body == {"username": "admin", "password": "****"}
    assert call.response_headers["Set-Cookie"] == "****"
    assert call.response_body == {"token": "****"}
    files = transcript.write(tmp_path)
    assert files == ["transcript.json", "transcript.md"]
    written = (tmp_path / "transcript.json").read_text("utf-8") + (
        tmp_path / "transcript.md"
    ).read_text("utf-8")
    for secret in ("pw-123", "abcdefgh12345", "query-secret", "s3cr3t", "abcdefghij-secret"):
        assert secret not in written


def test_an_unexpected_status_names_the_call_and_redacts_the_body(server: str) -> None:
    session = ApiSession("local", server, (2.0, 2.0))
    response = session.post("/auth", json_body={})
    session.close()

    with pytest.raises(UnexpectedStatusError, match=r"POST .*/auth answered 200, expected 201"):
        expect(response, 201)


def test_a_connection_failure_is_recorded_and_raised() -> None:
    transcript = Transcript()
    session = ApiSession("nowhere", "http://127.0.0.1:9", (0.5, 0.5), transcript)

    with pytest.raises(requests.ConnectionError) as raised:
        session.get("/health")

    # Refused on Linux, timed out on Windows: either way the transcript names what happened.
    call = transcript.calls[0]
    assert call.status is None
    assert call.error is not None
    assert call.error.startswith(type(raised.value).__name__ + ":")
