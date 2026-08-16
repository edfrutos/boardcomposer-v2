import subprocess
import urllib.error
from unittest.mock import patch

import pytest

from studio.update_installer import DownloadError, download_dmg, open_in_finder


class _FakeResponse:
    def __init__(self, body: bytes, *, content_length: int | None = None):
        self._chunks = [body[i : i + 4] for i in range(0, len(body), 4)]
        self.headers = {}
        if content_length is not None:
            self.headers["Content-Length"] = str(content_length)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, size=None):  # noqa: ARG002 — chunk size fixed by the fake
        if not self._chunks:
            return b""
        return self._chunks.pop(0)


def _fake_urlopen(response: _FakeResponse):
    def _open(request, timeout=None, context=None):  # noqa: ARG001
        return response

    return _open


def test_download_dmg_writes_the_full_body_under_the_urls_filename(tmp_path):
    body = b"fake dmg contents" * 100
    response = _FakeResponse(body, content_length=len(body))

    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(response)):
        dest_path = download_dmg(
            "https://example.com/releases/BoardComposerStudio-macos.dmg", tmp_path
        )

    assert dest_path == tmp_path / "BoardComposerStudio-macos.dmg"
    assert dest_path.read_bytes() == body
    assert not dest_path.with_name(dest_path.name + ".part").exists()


def test_download_dmg_reports_progress_as_chunks_arrive(tmp_path):
    body = b"x" * 40
    response = _FakeResponse(body, content_length=len(body))
    calls = []

    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(response)):
        download_dmg(
            "https://example.com/a.dmg",
            tmp_path,
            progress_callback=lambda read, total: calls.append((read, total)),
        )

    assert calls[-1] == (len(body), len(body))
    assert all(total == len(body) for _, total in calls)


def test_download_dmg_can_be_cancelled_mid_transfer_and_leaves_no_partial_file(
    tmp_path,
):
    body = b"x" * 40
    response = _FakeResponse(body, content_length=len(body))
    reads_seen = []

    def _should_cancel():
        return len(reads_seen) >= 2

    def _progress(read, total):  # noqa: ARG001
        reads_seen.append(read)

    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(response)):
        with pytest.raises(DownloadError):
            download_dmg(
                "https://example.com/a.dmg",
                tmp_path,
                progress_callback=_progress,
                should_cancel=_should_cancel,
            )

    assert not (tmp_path / "a.dmg").exists()
    assert not (tmp_path / "a.dmg.part").exists()


def test_download_dmg_network_failure_raises_download_error_not_the_raw_urllib_error(
    tmp_path,
):
    def _raise(request, timeout=None, context=None):  # noqa: ARG001
        raise urllib.error.URLError("no route to host")

    with patch("urllib.request.urlopen", side_effect=_raise):
        with pytest.raises(DownloadError, match="no route to host"):
            download_dmg("https://example.com/a.dmg", tmp_path)

    assert not (tmp_path / "a.dmg.part").exists()


def test_open_in_finder_runs_the_macos_open_command(tmp_path):
    dmg_path = tmp_path / "BoardComposerStudio-macos.dmg"
    dmg_path.write_bytes(b"")

    with patch("subprocess.run") as mock_run:
        open_in_finder(dmg_path)

    mock_run.assert_called_once_with(["open", str(dmg_path)], check=True)


def test_open_in_finder_propagates_a_failure_to_open(tmp_path):
    dmg_path = tmp_path / "BoardComposerStudio-macos.dmg"
    dmg_path.write_bytes(b"")

    with patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(1, ["open"]),
    ):
        with pytest.raises(subprocess.CalledProcessError):
            open_in_finder(dmg_path)
