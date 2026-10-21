"""Masks secrets before evidence is written: credential headers, cookies, token and password
fields, token query parameters and bearer tokens. Used on transcripts, console logs, page
sources, HAR files and Playwright traces (which Playwright writes with raw cookies). The rules
are the same as the UI flagship's `redact.ts`. Unit tests: tests/unit/test_redaction.py.
"""

import io
import json
import re
import zipfile
from typing import Any

MASK = "****"

SECRET_HEADERS = frozenset(
    {"authorization", "proxy-authorization", "cookie", "set-cookie", "x-api-key"}
)
# Header values that would name infrastructure (the live site's policies): never stored.
POLICY_HEADERS = frozenset(
    {"content-security-policy", "content-security-policy-report-only", "report-to", "nel"}
)
_SECRET_FIELD = re.compile(
    r"^(password|token|accesstoken|refreshtoken|idtoken|secret|apikey|authorization)$", re.I
)
_SECRET_QUERY = re.compile(
    r"([?&](?:token|access_token|api_key|apikey|key|password)=)[^&#\s\"']*", re.I
)
_SECRET_JSON_TEXT = re.compile(
    r"(\"(?:password|token|accessToken|refreshToken|secret|apiKey)\"\s*:\s*\")[^\"]*(\")", re.I
)
_HEADER_LINE = re.compile(
    r"^(\s*(?:authorization|proxy-authorization|cookie|set-cookie|x-api-key)\s*:\s*)"
    r"(?:(bearer|basic)\s+)?\S.*$",
    re.I | re.M,
)
_BEARER = re.compile(r"\b(bearer)\s+[A-Za-z0-9._~+/=-]{8,}", re.I)
_PASSWORD_INPUT = re.compile(r"(<input[^>]*type=\"password\"[^>]*value=\")[^\"]*(\")", re.I)


def redact_header(name: str, value: str) -> str:
    """A header value with secrets masked; the scheme of an Authorization header is kept."""
    lower = name.lower()
    if lower in POLICY_HEADERS:
        return "[policy not stored]"
    if lower not in SECRET_HEADERS:
        return value
    scheme, _, rest = value.partition(" ")
    return f"{scheme} {MASK}" if lower == "authorization" and rest else MASK


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {name: redact_header(name, value) for name, value in headers.items()}


def redact_text(text: str) -> str:
    out = _SECRET_QUERY.sub(rf"\g<1>{MASK}", text)
    out = _SECRET_JSON_TEXT.sub(rf"\g<1>{MASK}\g<2>", out)
    out = _PASSWORD_INPUT.sub(rf"\g<1>{MASK}\g<2>", out)
    out = _HEADER_LINE.sub(
        lambda m: f"{m.group(1)}{m.group(2)} {MASK}" if m.group(2) else f"{m.group(1)}{MASK}",
        out,
    )
    return _BEARER.sub(rf"\g<1> {MASK}", out)


def redact_json(value: Any) -> Any:
    """Any JSON value: secret fields masked, header pairs masked by name, cookies always."""
    return _redact_deep(value, is_cookie=False)


def _redact_deep(value: Any, *, is_cookie: bool) -> Any:
    if isinstance(value, list):
        return [_redact_deep(item, is_cookie=is_cookie) for item in value]
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, child in value.items():
            if _SECRET_FIELD.match(key) and not isinstance(child, (dict, list)):
                out[key] = MASK
            else:
                out[key] = _redact_deep(child, is_cookie=key.lower() == "cookies")
        name, header_value = value.get("name"), value.get("value")
        if isinstance(name, str) and isinstance(header_value, str):
            out["value"] = (
                MASK if is_cookie or "domain" in value else redact_header(name, header_value)
            )
        return out
    if isinstance(value, str):
        return redact_text(value)
    return value


def redact_har(har: dict[str, Any]) -> dict[str, Any]:
    """A HAR document with headers, cookies, URLs and bodies masked."""

    def clean(message: dict[str, Any] | None) -> None:
        if not message:
            return
        message["headers"] = [
            {"name": h["name"], "value": redact_header(h["name"], h["value"])}
            for h in message.get("headers", [])
        ]
        message["cookies"] = []
        if isinstance(message.get("url"), str):
            message["url"] = redact_text(message["url"])
        for body_key in ("postData", "content"):
            body = message.get(body_key)
            if isinstance(body, dict) and isinstance(body.get("text"), str):
                body["text"] = redact_text(body["text"])

    for entry in har.get("log", {}).get("entries", []):
        clean(entry.get("request"))
        clean(entry.get("response"))
    return har


def _is_binary(data: bytes) -> bool:
    return b"\x00" in data[:4096]


def redact_trace(data: bytes) -> bytes:
    """A Playwright trace zip with the same masking as a HAR. Event and network logs (JSON
    lines) are walked value by value; other text resources are redacted as text; images and
    other binary resources are kept as they are."""
    out = io.BytesIO()
    with (
        zipfile.ZipFile(io.BytesIO(data)) as source,
        zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as target,
    ):
        for info in source.infolist():
            content = source.read(info.filename)
            if re.search(r"\.(trace|network|stacks)$", info.filename):
                lines = []
                for line in content.decode("utf-8").split("\n"):
                    try:
                        lines.append(json.dumps(redact_json(json.loads(line))) if line else line)
                    except json.JSONDecodeError:
                        lines.append(redact_text(line))
                content = "\n".join(lines).encode("utf-8")
            elif not _is_binary(content):
                content = redact_text(content.decode("utf-8", errors="replace")).encode("utf-8")
            target.writestr(info.filename, content)
    return out.getvalue()
