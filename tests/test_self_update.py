import plistlib
import shutil
import subprocess
from pathlib import Path

import pytest

from studio.self_update import (
    SelfUpdateError,
    install_update,
    relaunch,
    running_app_bundle_path,
)


def _make_app_bundle(path: Path, version: str) -> Path:
    contents = path / "Contents"
    contents.mkdir(parents=True)
    with (contents / "Info.plist").open("wb") as file:
        plistlib.dump({"CFBundleShortVersionString": version}, file)
    return path


def _fake_subprocess_run(mount_contents: list[Path]):
    """Stands in for hdiutil/ditto: "mounting" copies fixture .app bundles
    into the requested mountpoint, "ditto" copies for real — both just
    directory copies, which is all install_update's orchestration cares
    about; no real disk image is involved in these tests."""

    def _run(args, capture_output=True, text=True):  # noqa: ARG001
        if args[0] == "hdiutil" and args[1] == "attach":
            mount_point = Path(args[args.index("-mountpoint") + 1])
            for app in mount_contents:
                shutil.copytree(app, mount_point / app.name)
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        if args[0] == "hdiutil" and args[1] == "detach":
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        if args[0] == "ditto":
            shutil.copytree(Path(args[1]), Path(args[2]))
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        raise AssertionError(f"unexpected subprocess.run call: {args}")

    return _run


def test_running_app_bundle_path_detects_a_macos_bundle(monkeypatch):
    monkeypatch.setattr(
        "sys.executable",
        "/Applications/BoardComposer Studio.app/Contents/MacOS/BoardComposerStudio",
    )

    assert running_app_bundle_path() == Path("/Applications/BoardComposer Studio.app")


def test_running_app_bundle_path_returns_none_outside_a_bundle(monkeypatch):
    monkeypatch.setattr("sys.executable", "/usr/bin/python3")

    assert running_app_bundle_path() is None


def test_install_update_replaces_the_bundle_and_returns_its_path(tmp_path, monkeypatch):
    current_bundle = _make_app_bundle(
        tmp_path / "BoardComposerStudio.app", version="0.3.25"
    )
    new_bundle_source = _make_app_bundle(
        tmp_path / "dmg_contents" / "BoardComposerStudio.app", version="0.3.26"
    )
    monkeypatch.setattr(subprocess, "run", _fake_subprocess_run([new_bundle_source]))

    result = install_update(
        tmp_path / "fake.dmg",
        current_bundle=current_bundle,
        expected_version="0.3.26",
    )

    assert result == current_bundle
    with (current_bundle / "Contents" / "Info.plist").open("rb") as file:
        assert plistlib.load(file)["CFBundleShortVersionString"] == "0.3.26"
    # No leftover temp/old directories next to the bundle.
    assert list(tmp_path.glob(".BoardComposerStudio-*")) == []


def test_install_update_rejects_a_version_mismatch_and_leaves_the_old_bundle(
    tmp_path, monkeypatch
):
    current_bundle = _make_app_bundle(
        tmp_path / "BoardComposerStudio.app", version="0.3.25"
    )
    new_bundle_source = _make_app_bundle(
        tmp_path / "dmg_contents" / "BoardComposerStudio.app", version="0.3.26"
    )
    monkeypatch.setattr(subprocess, "run", _fake_subprocess_run([new_bundle_source]))

    with pytest.raises(SelfUpdateError, match="no coincide"):
        install_update(
            tmp_path / "fake.dmg",
            current_bundle=current_bundle,
            expected_version="9.9.9",
        )

    with (current_bundle / "Contents" / "Info.plist").open("rb") as file:
        assert plistlib.load(file)["CFBundleShortVersionString"] == "0.3.25"
    assert list(tmp_path.glob(".BoardComposerStudio-*")) == []


def test_install_update_requires_the_current_bundle_to_exist(tmp_path):
    with pytest.raises(SelfUpdateError, match="No se encuentra"):
        install_update(
            tmp_path / "fake.dmg",
            current_bundle=tmp_path / "Missing.app",
        )


def test_install_update_rejects_a_dmg_with_more_than_one_app(tmp_path, monkeypatch):
    current_bundle = _make_app_bundle(
        tmp_path / "BoardComposerStudio.app", version="0.3.25"
    )
    first = _make_app_bundle(tmp_path / "dmg_contents" / "One.app", version="0.3.26")
    second = _make_app_bundle(tmp_path / "dmg_contents" / "Two.app", version="0.3.26")
    monkeypatch.setattr(subprocess, "run", _fake_subprocess_run([first, second]))

    with pytest.raises(SelfUpdateError, match="exactamente un"):
        install_update(tmp_path / "fake.dmg", current_bundle=current_bundle)

    with (current_bundle / "Contents" / "Info.plist").open("rb") as file:
        assert plistlib.load(file)["CFBundleShortVersionString"] == "0.3.25"


def test_install_update_surfaces_a_ditto_failure(tmp_path, monkeypatch):
    current_bundle = _make_app_bundle(
        tmp_path / "BoardComposerStudio.app", version="0.3.25"
    )
    new_bundle_source = _make_app_bundle(
        tmp_path / "dmg_contents" / "BoardComposerStudio.app", version="0.3.26"
    )

    def _run(args, capture_output=True, text=True):  # noqa: ARG001
        if args[0] == "hdiutil" and args[1] == "attach":
            mount_point = Path(args[args.index("-mountpoint") + 1])
            shutil.copytree(new_bundle_source, mount_point / new_bundle_source.name)
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        if args[0] == "hdiutil" and args[1] == "detach":
            return subprocess.CompletedProcess(args, 0, stdout="", stderr="")
        if args[0] == "ditto":
            return subprocess.CompletedProcess(args, 1, stdout="", stderr="disk full")
        raise AssertionError(f"unexpected subprocess.run call: {args}")

    monkeypatch.setattr(subprocess, "run", _run)

    with pytest.raises(SelfUpdateError, match="disk full"):
        install_update(tmp_path / "fake.dmg", current_bundle=current_bundle)

    with (current_bundle / "Contents" / "Info.plist").open("rb") as file:
        assert plistlib.load(file)["CFBundleShortVersionString"] == "0.3.25"


def test_relaunch_opens_the_bundle_as_a_detached_process(tmp_path, monkeypatch):
    calls = []
    monkeypatch.setattr(
        subprocess,
        "Popen",
        lambda args, **kwargs: calls.append((args, kwargs)),
    )

    relaunch(tmp_path / "BoardComposerStudio.app")

    assert len(calls) == 1
    args, kwargs = calls[0]
    assert args == ["open", str(tmp_path / "BoardComposerStudio.app")]
    assert kwargs.get("start_new_session") is True
