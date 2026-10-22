"""Masks secrets before evidence is written: credential headers, cookies, token and password
fields, token query parameters, bearer tokens and the machine's own folders in paths. Used on
transcripts, console logs, page sources, HAR files and Playwright traces (which Playwright writes
with raw cookies). The rules are the same as the UI flagship's `redact.ts`. Unit tests:
tests/unit/test_redaction.py.
"""

import hashlib
import io
import json
import re
import sys
import tempfile
import zipfile
from pathlib import Path
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
# A home folder names the person who ran the tests (Playwright traces record temp paths):
# C:\Users\<name> (also with JSON's doubled backslashes), /home/<name>, /Users/<name>.
_WINDOWS_HOME = re.compile(r"([A-Za-z]:(\\{1,2})Users\2)([^\\/\"'\s<>]+)", re.I)
_UNIX_HOME = re.compile(r"((?<![\w/.])/(?:home|Users)/)([^/\"'\s<>]+)")
USER = "<user>"

# The folders of the machine that ran the tests, most specific first: the repository (paths
# under it become relative), the temp folder and the home folder. Stack traces and Playwright's
# traces carry them. Each is (path, replacement); "" makes the paths under it relative.
REPO_ROOT = Path(__file__).resolve().parents[3]
LOCAL_ROOTS = [(str(REPO_ROOT), ""), (tempfile.gettempdir(), "<tmp>"), (str(Path.home()), "~")]
# One separator as text or JSON text writes it: /, \ or \\.
_SEP = r"(?:\\{1,2}|/)"


def _root_pattern(path: str, ignore_case: bool) -> re.Pattern[str] | None:
    parts = [part for part in re.split(r"[\\/]+", path) if part]
    if len(parts) < 2:  # never "/" or "C:\" alone
        return None
    lead = _SEP if re.match(r"[\\/]", path) else ""
    body = f"{_SEP}+".join(re.escape(part) for part in parts)
    return re.compile(rf"{lead}{body}(?![\w.-])({_SEP})?", re.I if ignore_case else 0)


def redact_local_paths(
    text: str,
    roots: list[tuple[str, str]] | None = None,
    ignore_case: bool = sys.platform == "win32",
) -> str:
    """Replaces each local root in `text` (paths under the repository become relative)."""
    out = text
    for path, replacement in LOCAL_ROOTS if roots is None else roots:
        pattern = _root_pattern(path, ignore_case)
        if pattern is None:
            continue

        def replace(match: re.Match[str], replacement: str = replacement) -> str:
            sep = match.group(1) or ""
            if replacement:
                return replacement + sep
            return "" if sep else "."

        out = pattern.sub(replace, out)
    return out


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
    out = _SECRET_QUERY.sub(rf"\g<1>{MASK}", redact_local_paths(text))
    out = _SECRET_JSON_TEXT.sub(rf"\g<1>{MASK}\g<2>", out)
    out = _PASSWORD_INPUT.sub(rf"\g<1>{MASK}\g<2>", out)
    out = _WINDOWS_HOME.sub(rf"\g<1>{USER}", out)
    out = _UNIX_HOME.sub(rf"\g<1>{USER}", out)
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


def _sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()


def _trace_strings(source: zipfile.ZipFile) -> set[str]:
    """Every string anywhere in the JSON lines of a trace's event and stack logs."""
    found: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, str):
            found.add(value)
        elif isinstance(value, list):
            for item in value:
                walk(item)
        elif isinstance(value, dict):
            for item in value.values():
                walk(item)

    for name in source.namelist():
        if re.search(r"\.(trace|stacks)$", name):
            for line in source.read(name).decode("utf-8").split("\n"):
                try:
                    walk(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return found


def _renamed_sources(source: zipfile.ZipFile) -> dict[str, str]:
    """The trace viewer finds a test's source file at `src/<sha1 of its path>.<ext>`. Paths are
    redacted, so each source is renamed to the hash of its redacted path; the viewer's Source tab
    keeps working."""
    sources = {}
    for name in source.namelist():
        match = re.fullmatch(r"src/([0-9a-f]{40})(\.[^/]*)?", name)
        if match:
            sources[match.group(1)] = (name, match.group(2) or "")
    renames: dict[str, str] = {}
    if not sources:
        return renames
    for path in _trace_strings(source):
        found = sources.get(_sha1(path))
        clean = redact_local_paths(path)
        if found and clean != path:
            renames[found[0]] = f"src/{_sha1(clean)}{found[1]}"
    return renames


def redact_trace(data: bytes) -> bytes:
    """A Playwright trace zip with the same masking as a HAR. Event and network logs (JSON
    lines) are walked value by value; other text resources are redacted as text; images and
    other binary resources are kept as they are."""
    out = io.BytesIO()
    with (
        zipfile.ZipFile(io.BytesIO(data)) as source,
        zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as target,
    ):
        renames = _renamed_sources(source)
        for info in source.infolist():
            content = source.read(info.filename)
            name = renames.get(info.filename, info.filename)
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
            target.writestr(name, content)
    return out.getvalue()
