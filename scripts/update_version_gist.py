"""Publishes the current release's version.json to the public update Gist.

Run from package-studio.yml after a release's .dmg has been uploaded to
the public boardcomposer-releases repo. Stdlib-only (no `requests`) so it
needs nothing beyond what CI already installs.

Exists to close DT-0028: before this, the Gist that
studio/update_check.py reads (docs/masterplan/DOC-006-DeudaTecnica.md)
was a manual step in the release checklist — easy to forget, and
forgetting it silently, since a stale Gist doesn't error, it just tells
users truthfully-but-wrongly that they're already up to date.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

GIST_ID = "65bd1ae68d45dc9bee418622c39ca8b7"
SOURCE_REPO = "edfrutos/boardcomposer-v2"
RELEASES_REPO = "edfrutos/boardcomposer-releases"
DMG_ASSET_NAME = "BoardComposerStudio-macos.dmg"


def main() -> int:
    token = os.environ.get("GH_TOKEN")
    tag = os.environ.get("RELEASE_TAG")
    if not token:
        print("GH_TOKEN no está definido — nada que hacer.")
        return 0
    if not tag:
        print("RELEASE_TAG no está definido.", file=sys.stderr)
        return 1

    version = tag.lstrip("vV")
    payload = {
        "version": version,
        "release_url": f"https://github.com/{SOURCE_REPO}/releases/tag/{tag}",
        "dmg_url": (
            f"https://github.com/{RELEASES_REPO}/releases/download/"
            f"{tag}/{DMG_ASSET_NAME}"
        ),
    }
    body = json.dumps(
        {"files": {"version.json": {"content": json.dumps(payload, indent=2) + "\n"}}}
    ).encode("utf-8")

    request = urllib.request.Request(
        f"https://api.github.com/gists/{GIST_ID}",
        data=body,
        method="PATCH",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "boardcomposer-release-ci",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response.read()
    except urllib.error.HTTPError as error:
        print(
            f"No se pudo actualizar el Gist ({error.code}): "
            f"{error.read().decode('utf-8', 'replace')}",
            file=sys.stderr,
        )
        return 1

    print(f"Gist actualizado a {version} ({payload['dmg_url']}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
