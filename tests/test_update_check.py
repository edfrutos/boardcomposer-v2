import json
import urllib.error
from unittest.mock import patch

from studio.update_check import _parse_version, check_for_update


def test_parse_version_orders_by_numeric_components():
    assert _parse_version("0.3.11") > _parse_version("0.3.9")
    assert _parse_version("0.3.2") < _parse_version("0.3.10")
    assert _parse_version("v0.3.5") == _parse_version("0.3.5")


def test_parse_version_tolerates_non_numeric_fragments():
    assert _parse_version("0.3.11-beta") == (0, 3, 11)
    assert _parse_version("") == (0,)


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self._payload).encode("utf-8")


def _fake_urlopen(payload: dict):
    def _open(request, timeout=None):  # noqa: ARG001
        return _FakeResponse(payload)

    return _open


def test_reports_an_update_when_the_latest_release_is_newer():
    payload = {"tag_name": "v0.3.12", "html_url": "https://example.com/v0.3.12"}
    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(payload)):
        result = check_for_update("0.3.11")

    assert result.checked_ok is True
    assert result.update_available is True
    assert result.latest_version == "0.3.12"
    assert result.release_url == "https://example.com/v0.3.12"


def test_reports_no_update_when_already_on_the_latest_release():
    payload = {"tag_name": "v0.3.11", "html_url": "https://example.com/v0.3.11"}
    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(payload)):
        result = check_for_update("0.3.11")

    assert result.checked_ok is True
    assert result.update_available is False


def test_reports_no_update_when_current_is_newer_than_latest_seen():
    # A dev build ahead of the last published tag shouldn't nag to
    # "upgrade" to an older release.
    payload = {"tag_name": "v0.3.9", "html_url": "https://example.com/v0.3.9"}
    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(payload)):
        result = check_for_update("0.3.11")

    assert result.checked_ok is True
    assert result.update_available is False


def test_network_failure_comes_back_as_a_result_not_an_exception():
    def _raise(request, timeout=None):  # noqa: ARG001
        raise urllib.error.URLError("no route to host")

    with patch("urllib.request.urlopen", side_effect=_raise):
        result = check_for_update("0.3.11")

    assert result.checked_ok is False
    assert result.update_available is False
    assert "no route to host" in result.error


def test_missing_tag_name_comes_back_as_a_result_not_an_exception():
    payload = {"html_url": "https://example.com"}
    with patch("urllib.request.urlopen", side_effect=_fake_urlopen(payload)):
        result = check_for_update("0.3.11")

    assert result.checked_ok is False
    assert result.error is not None
