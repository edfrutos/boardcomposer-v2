"""Downloads and opens a BoardComposer Studio .dmg update.

Qt-free on purpose, same split as studio/update_check.py: this only
downloads the file and hands it to Finder — MainWindow owns the
confirmation dialog and the thread that keeps the UI responsive during a
~130 MB download. Still not a self-updater: the app never replaces
itself in place, so this stays out of the Gatekeeper-after-self-replace
problem documented in DOC-999-Ideas.md ("Auto-actualización de
BoardComposer Studio"). The user still drags the app to Aplicaciones
from the mounted image — same manual step as always, just without
hunting for the release page by hand first.
"""

from __future__ import annotations

import ssl
import subprocess
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path

import certifi

REQUEST_TIMEOUT_SECONDS = 15.0
_CHUNK_SIZE = 256 * 1024

# Same reasoning as update_check.py's _SSL_CONTEXT (DT-0024): Nuitka's
# frozen .app doesn't see the OS/venv CA bundle a normal interpreter does.
_SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


class DownloadError(Exception):
    """Raised when the .dmg can't be downloaded — message is user-facing."""


def download_dmg(
    url: str,
    dest_dir: Path,
    *,
    progress_callback: Callable[[int, int], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
    timeout: float = REQUEST_TIMEOUT_SECONDS,
) -> Path:
    """Downloads `url` into `dest_dir`, keeping the URL's filename.

    Calls `progress_callback(bytes_read, total_bytes)` after each chunk —
    `total_bytes` is 0 if the server didn't send Content-Length. Checking
    `should_cancel()` between chunks lets a caller abort a large in-flight
    download instead of only refusing to start one. Writes to a `.part`
    file and renames on success, so a cancelled/failed download never
    leaves a file that looks complete.
    """
    filename = url.rsplit("/", 1)[-1] or "BoardComposerStudio-macos.dmg"
    dest_path = dest_dir / filename
    tmp_path = dest_path.with_name(dest_path.name + ".part")

    request = urllib.request.Request(
        url, headers={"User-Agent": "BoardComposer-Studio"}
    )

    try:
        with urllib.request.urlopen(
            request, timeout=timeout, context=_SSL_CONTEXT
        ) as response:
            total = int(response.headers.get("Content-Length") or 0)
            read = 0
            with open(tmp_path, "wb") as fh:
                while True:
                    if should_cancel is not None and should_cancel():
                        raise DownloadError("Descarga cancelada.")
                    chunk = response.read(_CHUNK_SIZE)
                    if not chunk:
                        break
                    fh.write(chunk)
                    read += len(chunk)
                    if progress_callback is not None:
                        progress_callback(read, total)
    except (urllib.error.URLError, OSError, TimeoutError) as error:
        tmp_path.unlink(missing_ok=True)
        raise DownloadError(
            f"No se pudo descargar la actualización.\n\n{error}"
        ) from error
    except DownloadError:
        tmp_path.unlink(missing_ok=True)
        raise

    tmp_path.replace(dest_path)
    return dest_path


def open_in_finder(path: Path) -> None:
    """Mounts/opens `path` (a .dmg) the same way double-clicking it in
    Finder would. macOS-only on purpose — same as the rest of Studio's
    packaging (Nuitka target is macOS/arm64 only, DT-0011)."""
    subprocess.run(["open", str(path)], check=True)
