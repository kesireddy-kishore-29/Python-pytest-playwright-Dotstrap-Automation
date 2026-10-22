"""Redaction: every text, JSON, HAR and trace written as evidence goes through these rules."""

import hashlib
import io
import json
import zipfile
from pathlib import Path

import pytest

from framework.core.redaction import (
    MASK,
    REPO_ROOT,
    redact_har,
    redact_header,
    redact_json,
    redact_local_paths,
    redact_text,
    redact_trace,
)

pytestmark = pytest.mark.unit

B = chr(0x5C)  # one backslash
WINDOWS_ROOTS = [
    (f"D:{B}work{B}repo", ""),
    (f"C:{B}Users{B}someone{B}AppData{B}Local{B}Temp", "<tmp>"),
    (f"C:{B}Users{B}someone", "~"),
]


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8"), usedforsecurity=False).hexdigest()


def test_paths_under_the_repository_become_relative_in_text_and_json_text() -> None:
    lines = [
        f"at open (D:{B}work{B}repo{B}src{B}pages{B}sauce.py:20)",
        f'{{"file":"D:{B * 2}work{B * 2}repo{B * 2}tests{B * 2}test_a.py"}}',
        "file:///D:/work/repo/src/a.py",
        f"cwd d:{B}work{B}repo",
    ]

    out = redact_local_paths("\n".join(lines), WINDOWS_ROOTS, ignore_case=True).split("\n")

    assert out == [
        f"at open (src{B}pages{B}sauce.py:20)",
        f'{{"file":"tests{B * 2}test_a.py"}}',
        "file:///src/a.py",
        "cwd .",
    ]


def test_the_temp_and_home_folders_are_replaced_so_no_user_name_is_left() -> None:
    text = (
        f'{{"dir":"C:{B * 2}Users{B * 2}someone{B * 2}AppData{B * 2}Local{B * 2}Temp{B * 2}pw-1"}}'
        f" C:{B}Users{B}someone{B}.cache"
    )

    out = redact_local_paths(text, WINDOWS_ROOTS, ignore_case=True)

    assert out == f'{{"dir":"<tmp>{B * 2}pw-1"}} ~{B}.cache'


def test_a_sibling_folder_that_only_starts_with_the_same_name_is_left_alone() -> None:
    text = f"D:{B}work{B}repo-other{B}x.py"

    assert redact_local_paths(text, WINDOWS_ROOTS, ignore_case=True) == text


def test_posix_paths_as_on_the_ci_runner() -> None:
    roots = [("/home/runner/work/r/r", ""), ("/home/runner", "~")]
    text = "/home/runner/work/r/r/tests/test_a.py /home/runner/.cache/x"

    assert redact_local_paths(text, roots, ignore_case=False) == "tests/test_a.py ~/.cache/x"


def test_this_machine_is_redacted_by_default() -> None:
    assert redact_text(str(REPO_ROOT / "src" / "x.py")) == str(Path("src") / "x.py")
    assert redact_text(str(Path.home() / "notes.txt")) == str(Path("~") / "notes.txt")


def test_trace_sources_are_renamed_to_the_hash_of_their_relative_path() -> None:
    file = str(REPO_ROOT / "tests" / "test_a.py")
    relative = str(Path("tests") / "test_a.py")
    source = io.BytesIO()
    with zipfile.ZipFile(source, "w") as archive:
        archive.writestr("trace.trace", json.dumps({"stack": [{"file": file, "line": 3}]}))
        archive.writestr("trace.stacks", json.dumps({"files": [file], "stacks": []}))
        archive.writestr(f"src/{sha1(file)}.py", "def test_a(): ...")

    redacted = zipfile.ZipFile(io.BytesIO(redact_trace(source.getvalue())))

    assert f"src/{sha1(relative)}.py" in redacted.namelist()
    assert f"src/{sha1(file)}.py" not in redacted.namelist()
    assert json.loads(redacted.read("trace.stacks")) == {"files": [relative], "stacks": []}
    assert json.dumps(str(REPO_ROOT))[1:-1] not in redacted.read("trace.trace").decode()


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


def test_home_folders_lose_the_user_name_but_urls_keep_their_paths() -> None:
    backslash = chr(0x5C)
    windows = (
        f"C:{backslash}Users{backslash}someone{backslash}AppData{backslash}Local{backslash}Temp"
    )
    escaped = windows.replace(backslash, backslash * 2)

    assert redact_text(windows) == windows.replace("someone", "<user>")
    assert redact_text(escaped) == escaped.replace("someone", "<user>")
    assert redact_text("/home/someone/work") == "/home/<user>/work"
    assert redact_text('"/Users/someone/x"') == '"/Users/<user>/x"'
    assert redact_text("http://localhost:4173/api/users/me") == "http://localhost:4173/api/users/me"


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
