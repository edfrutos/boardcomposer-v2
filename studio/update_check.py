"""Checks GitHub for a newer BoardComposer Studio release (IDE-0032).

Qt-free on purpose, same split as studio/panels/: this only figures out
*whether* an update exists, MainWindow decides how to show it. Never
downloads or installs anything — just points at the release page and lets
the user take it from there, so this doesn't need to get into
signing/notarization territory for a self-updater.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

LATEST_RELEASE_API_URL = (
    "https://api.github.com/repos/edfrutos/boardcomposer-v2/releases/latest"
)
REQUEST_TIMEOUT_SECONDS = 5.0


@dataclass(frozen=True)
class UpdateCheckResult:
    checked_ok: bool
    update_available: bool
    current_version: str
    latest_version: str | None = None
    release_url: str | None = None
    error: str | None = None


def _parse_version(version: str) -> tuple[int, ...]:
    """"0.3.11" -> (0, 3, 11). Non-numeric fragments fall back to 0 instead
    of raising — this only ever has to answer "is A newer than B", not
    validate that a version string is well-formed."""
    parts = []
    for chunk in version.strip().lstrip("vV").split("."):
        digits = "".join(char for char in chunk if char.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def check_for_update(
    current_version: str, *, timeout: float = REQUEST_TIMEOUT_SECONDS
) -> UpdateCheckResult:
    """Compares `current_version` against the latest published GitHub
    release. Never raises — network/parsing failures come back as a result
    with checked_ok=False rather than an exception, so a caller on the UI
    thread can show a plain message instead of a stack trace."""
    request = urllib.request.Request(
        LATEST_RELEASE_API_URL,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "BoardComposer-Studio",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except (urllib.error.URLError, OSError, ValueError, TimeoutError) as error:
        return UpdateCheckResult(
            checked_ok=False,
            update_available=False,
            current_version=current_version,
            error=str(error),
        )

    latest_version = str(payload.get("tag_name") or "").lstrip("vV") or None
    if latest_version is None:
        return UpdateCheckResult(
            checked_ok=False,
            update_available=False,
            current_version=current_version,
            error="La respuesta de GitHub no incluía una versión (tag_name).",
        )

    return UpdateCheckResult(
        checked_ok=True,
        update_available=_parse_version(latest_version)
        > _parse_version(current_version),
        current_version=current_version,
        latest_version=latest_version,
        release_url=payload.get("html_url"),
    )
