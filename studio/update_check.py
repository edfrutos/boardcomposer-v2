"""Checks for a newer BoardComposer Studio release (IDE-0032).

Qt-free on purpose, same split as studio/panels/: this only figures out
*whether* an update exists, MainWindow decides how to show it (and,
since the download itself is a separate concern, studio/update_installer.py
decides how to fetch the .dmg this points at).

Points at a public Gist (`version.json`), not the GitHub Releases API
(DT-0025): the repo itself is private, so an unauthenticated request to
`/repos/.../releases/latest` gets a 404 — GitHub returns that instead of
403 for a private resource, specifically so an outsider can't even tell
it exists. Embedding a token in a binary anyone can download and
disassemble isn't an acceptable fix, so instead a single small public
file carries the version number, the release page's URL, and (DT-0028)
the direct download URL of the .dmg — nothing about the private repo's
contents. `dmg_url` points at a *second*, equally public repo
(edfrutos/boardcomposer-releases) that holds nothing but the binaries:
release assets of a private repo require authentication to download
(same 404-for-privacy behavior as the Releases API above), so the .dmg
itself has to live somewhere public too, separate from the source. The
gist's own history stays as a changelog of past "latest version"
values, which is fine to be public even though the code behind it isn't.
"""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from dataclasses import dataclass

import certifi

LATEST_VERSION_URL = (
    "https://gist.githubusercontent.com/edfrutos/"
    "65bd1ae68d45dc9bee418622c39ca8b7/raw/version.json"
)
REQUEST_TIMEOUT_SECONDS = 5.0

# Nuitka's frozen .app doesn't see the CA bundle a normal interpreter does
# (same category of "works from source, breaks once packaged" as DT-0023):
# urlopen()'s default SSLContext failed with CERTIFICATE_VERIFY_FAILED for
# a real user, reported with a screenshot, even though the request works
# fine from this venv. certifi is already installed transitively (the AI
# provider SDKs pull it in) — pointing the context at its bundle explicitly
# doesn't depend on Nuitka finding whatever the OS/venv would have used.
_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


@dataclass(frozen=True)
class UpdateCheckResult:
    checked_ok: bool
    update_available: bool
    current_version: str
    latest_version: str | None = None
    release_url: str | None = None
    dmg_url: str | None = None
    error: str | None = None


def _parse_version(version: str) -> tuple[int, ...]:
    """ "0.3.11" -> (0, 3, 11). Non-numeric fragments fall back to 0 instead
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
    """Compares `current_version` against the version published in the
    public Gist (see module docstring). Never raises — network/parsing
    failures come back as a result with checked_ok=False rather than an
    exception, so a caller on the UI thread can show a plain message
    instead of a stack trace."""
    request = urllib.request.Request(
        LATEST_VERSION_URL,
        headers={"User-Agent": "BoardComposer-Studio"},
    )

    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=_SSL_CONTEXT
        ) as response:
            payload = json.load(response)
    except (urllib.error.URLError, OSError, ValueError, TimeoutError) as error:
        return UpdateCheckResult(
            checked_ok=False,
            update_available=False,
            current_version=current_version,
            error=str(error),
        )

    latest_version = str(payload.get("version") or "").lstrip("vV") or None
    if latest_version is None:
        return UpdateCheckResult(
            checked_ok=False,
            update_available=False,
            current_version=current_version,
            error="El fichero de versión no incluía un campo 'version'.",
        )

    return UpdateCheckResult(
        checked_ok=True,
        update_available=_parse_version(latest_version)
        > _parse_version(current_version),
        current_version=current_version,
        latest_version=latest_version,
        release_url=payload.get("release_url"),
        dmg_url=payload.get("dmg_url"),
    )
