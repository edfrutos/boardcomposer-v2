"""Replaces the running .app with a downloaded update and relaunches it.

Qt-free, same split as update_check.py/update_installer.py: this only
does the file surgery — MainWindow decides when it's safe to run it (the
project must already be saved-or-discarded; see
MainWindow._maybe_save_and_confirm_close()) and quits the process
afterwards.

Not Sparkle: Sparkle is built for Xcode-produced bundles and ships its
own signed helper processes (Autoupdate.app, XPC services) to survive
the host app quitting. Embedding that into a Nuitka-frozen bundle would
mean codesigning third-party components inside our own bundle — the
same category of fragile that surfaced three real bugs the first time
this project signed against a real certificate (DT-0011). Instead this
replaces the bundle *before* quitting: on macOS/APFS, deleting or
renaming a file out from under the process currently executing it is
safe — the running process keeps its already-mapped pages via the old
inode until it exits, so there is no window where the app is "using" a
half-replaced bundle. No new update-signing key is needed either — the
.dmg being installed is the same one CI already signs and notarizes for
manual installs (IDE-0043); the trust anchor here is unchanged.

Deliberately doesn't keep a `.app.bak` for the user to roll back to by
hand (explicit product choice) — the old bundle is renamed aside only
long enough to make the final rename atomic, then deleted immediately.
"""

from __future__ import annotations

import os
import plistlib
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

_APP_BUNDLE_MARKER = ".app/Contents/MacOS"


class SelfUpdateError(Exception):
    """Raised when installing the update fails — message is user-facing."""


def running_app_bundle_path() -> Path | None:
    """The `.app` bundle currently executing, or None outside one (running
    from source, a test, or a non-macOS platform) — the caller uses this
    to decide whether self-update is even possible, falling back to the
    manual download-and-open flow otherwise."""
    executable = str(Path(sys.executable).resolve())
    index = executable.find(_APP_BUNDLE_MARKER)
    if index == -1:
        return None
    return Path(executable[: index + len(".app")])


def _mount_dmg(dmg_path: Path) -> Path:
    mount_point = Path(tempfile.mkdtemp(prefix="boardcomposer-update-mount-"))
    result = subprocess.run(
        [
            "hdiutil",
            "attach",
            "-nobrowse",
            "-mountpoint",
            str(mount_point),
            str(dmg_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise SelfUpdateError(
            f"No se pudo montar la actualización descargada.\n\n{result.stderr}"
        )
    return mount_point


def _unmount_dmg(mount_point: Path) -> None:
    # Best-effort: by the time this runs we already have what we need off
    # the image, so a failure here shouldn't block the install.
    subprocess.run(
        ["hdiutil", "detach", str(mount_point), "-quiet"],
        capture_output=True,
        text=True,
    )


def _find_app_bundle(mount_point: Path) -> Path:
    candidates = sorted(mount_point.glob("*.app"))
    if len(candidates) != 1:
        raise SelfUpdateError(
            "La imagen de la actualización no contiene exactamente un "
            f".app (encontrados: {len(candidates)})."
        )
    return candidates[0]


def _copy_app_bundle(source: Path, dest: Path) -> None:
    # ditto (not shutil.copytree/cp -R): Apple's own tool for copying app
    # bundles, preserves the extended attributes and resource forks a
    # code signature depends on.
    result = subprocess.run(
        ["ditto", str(source), str(dest)], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise SelfUpdateError(f"No se pudo copiar la actualización.\n\n{result.stderr}")


def _bundle_version(bundle: Path) -> str | None:
    plist_path = bundle / "Contents" / "Info.plist"
    if not plist_path.exists():
        return None
    with plist_path.open("rb") as file:
        return plistlib.load(file).get("CFBundleShortVersionString")


def install_update(
    dmg_path: Path, *, current_bundle: Path, expected_version: str | None = None
) -> Path:
    """Replaces `current_bundle` in place with the .app inside `dmg_path`.

    Never leaves `current_bundle` missing: the old bundle is only removed
    after the new one is fully copied, version-checked (if
    `expected_version` is given) and already renamed into its place — the
    two renames below are same-directory, so each one is atomic. Raises
    SelfUpdateError (message safe to show the user) on any failure;
    `current_bundle` is left untouched by every failure path.
    """
    if not current_bundle.exists():
        raise SelfUpdateError(f"No se encuentra la app instalada en {current_bundle}.")

    mount_point = _mount_dmg(dmg_path)
    temp_target = current_bundle.parent / f".{current_bundle.stem}-update-{os.getpid()}"
    try:
        source_bundle = _find_app_bundle(mount_point)
        if temp_target.exists():
            shutil.rmtree(temp_target)
        _copy_app_bundle(source_bundle, temp_target)
    except SelfUpdateError:
        shutil.rmtree(temp_target, ignore_errors=True)
        raise
    finally:
        _unmount_dmg(mount_point)

    if expected_version is not None:
        actual_version = _bundle_version(temp_target)
        if actual_version != expected_version:
            shutil.rmtree(temp_target, ignore_errors=True)
            raise SelfUpdateError(
                "La actualización descargada no coincide con la versión "
                f"esperada ({expected_version} vs {actual_version}) — "
                "cancelada para no dejar una instalación a medias."
            )

    old_target = current_bundle.parent / f".{current_bundle.stem}-old-{os.getpid()}"
    try:
        current_bundle.rename(old_target)
    except OSError as error:
        shutil.rmtree(temp_target, ignore_errors=True)
        raise SelfUpdateError(
            f"No se pudo preparar la instalación en {current_bundle} — "
            f"¿tienes permiso de escritura ahí?\n\n{error}"
        ) from error

    try:
        temp_target.rename(current_bundle)
    except OSError as error:
        old_target.rename(current_bundle)
        raise SelfUpdateError(
            f"No se pudo completar la instalación en {current_bundle}.\n\n{error}"
        ) from error

    shutil.rmtree(old_target, ignore_errors=True)
    return current_bundle


def relaunch(bundle: Path, *, wait_for_pid: int | None = None) -> None:
    """Starts the new bundle as an independent process (detached from this
    one, `start_new_session=True`) so it keeps running after this process
    exits — the caller quits right after calling this.

    `wait_for_pid`, when given, is this process's own pid: calling `open`
    for the *same bundle path* while this process is still alive races
    Launch Services' "is this app already running" check, which can just
    activate (or no-op on) the almost-dead old instance instead of
    starting a new one — the launch silently does nothing (confirmed:
    the file swap itself completes, but the app never reappears). A
    detached shell polls for that pid to actually disappear before
    calling `open -n` (force a new instance, in case Launch Services is
    still confused about a just-vacated bundle identifier), so the
    launch only ever happens once this process is truly gone.
    """
    if wait_for_pid is None:
        subprocess.Popen(["open", "-n", str(bundle)], start_new_session=True)
        return

    script = (
        f"while kill -0 {wait_for_pid} 2>/dev/null; do sleep 0.2; done; "
        f"open -n {shlex.quote(str(bundle))}"
    )
    subprocess.Popen(["/bin/sh", "-c", script], start_new_session=True)
