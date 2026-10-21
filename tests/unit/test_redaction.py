"""Redaction: every text, JSON, HAR and trace written as evidence goes through these rules."""

import io
import json
import zipfile

import pytest

from framework.core.redaction import (
    MASK,
    redact_har,
    redact_header,
    redact_json,
    redact_text,
    redact_trace,
)

pytestmark = pytest.mark.unit


def test_credential_headers_are_masked_and_the_scheme_kept() -> None:
    assert redact_header("Authorization", "Bearer abc.def.ghi") == f"Bearer {MASK}"
    assert redact_header("Cookie", "token=abc; other=1") == MASK
    assert redact_header("Set-Cookie", "sutui_session=xyz; HttpOnly") == MASK
    assert redact_header("Accept", "application/json") == "application/json"


def test_policy_headers_are_never_stored() -> None:
    assert redact_header("Content-Security-Policy", "default-src 'self'") == "[policy not stored]"


def test_secret_json_fields_and_cookie_lists_are_masked() -> None:
    value = {
        "password": "pw-123",
        "accessToken": "t0k3n",
        "user": {"email": "a@example.test"},
        "cookies": [{"name": "sutui_session", "value": "s3cr3t", "domain": "localhost"}],
        "headers": [{"name": "Cookie", "value": "a=b"}, {"name": "Accept", "value": "*/*"}],
    }

    out = redact_json(value)

    assert out["password"] == MASK
    assert out["accessToken"] == MASK
    assert out["user"] == {"email": "a@example.test"}
    assert out["cookies"][0]["value"] == MASK
    assert out["headers"] == [
        {"name": "Cookie", "value": MASK},
        {"name": "Accept", "value": "*/*"},
    ]


def test_free_text_secrets_are_masked() -> None:
    text = (
        "GET https://x.test/a?universe=U&token=abc123&b=2\n"
        "authorization: Bearer eyJhbGciOiJIUzI1NiJ9.e30.sig\n"
        '{"password":"pw-1"}\n'
        '<input type="password" value="secret_sauce">'
    )

    out = redact_text(text)

    assert "token=****&b=2" in out
    assert "authorization: bearer ****" in out.lower()
    assert '"password":"****"' in out
    assert 'value="****"' in out
    assert "abc123" not in out
    assert "secret_sauce" not in out


def test_ordinary_text_is_left_alone() -> None:
    text = "6 products sorted by price; a token of thanks"

    assert redact_text(text) == text


def test_a_har_loses_headers_cookies_and_secret_bodies() -> None:
    har = {
        "log": {
            "entries": [
                {
                    "request": {
                        "url": "https://x.test/api?token=abc",
                        "headers": [{"name": "Authorization", "value": "Bearer abcdefgh123"}],
                        "cookies": [{"name": "sid", "value": "1"}],
                        "postData": {"text": '{"password":"pw"}'},
                    },
                    "response": {
                        "headers": [{"name": "Set-Cookie", "value": "sid=1"}],
                        "cookies": [{"name": "sid", "value": "1"}],
                        "content": {"text": '{"token":"t"}'},
                    },
                }
            ]
        }
    }

    entry = redact_har(har)["log"]["entries"][0]

    assert entry["request"]["url"] == "https://x.test/api?token=****"
    assert entry["request"]["headers"] == [{"name": "Authorization", "value": f"Bearer {MASK}"}]
    assert entry["request"]["cookies"] == []
    assert entry["request"]["postData"]["text"] == '{"password":"****"}'
    assert entry["response"]["headers"] == [{"name": "Set-Cookie", "value": MASK}]
    assert entry["response"]["content"]["text"] == '{"token":"****"}'


def test_a_trace_is_redacted_line_by_line_and_binaries_are_kept() -> None:
    source = io.BytesIO()
    event = {"type": "context-options", "storageState": {"cookies": []}}
    cookie = {"name": "sutui_session", "value": "raw-session-value-123", "domain": "localhost"}
    network = {"request": {"headers": [{"name": "cookie", "value": "sutui_session=raw"}]}}
    image = b"\x89PNG\x00\x00binary"
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("trace.trace", json.dumps(event) + "\n" + json.dumps({"c": [cookie]}))
        archive.writestr("trace.network", json.dumps(network))
        archive.writestr("resources/page.html", '<a href="/x?token=abc123">x</a>')
        archive.writestr("resources/shot.png", image)

    redacted = zipfile.ZipFile(io.BytesIO(redact_trace(source.getvalue())))

    trace = redacted.read("trace.trace").decode()
    assert "raw-session-value-123" not in trace
    assert json.loads(trace.splitlines()[1])["c"][0]["value"] == MASK
    assert "sutui_session=raw" not in redacted.read("trace.network").decode()
    assert redacted.read("resources/page.html").decode() == '<a href="/x?token=****">x</a>'
    assert redacted.read("resources/shot.png") == image
