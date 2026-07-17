from boardcomposer.plugin_visibility import plugin_summary
from boardcomposer.plugins import PluginLoadError


def _patch_all_groups(monkeypatch, plugins=None, errors=None):
    plugins = plugins or {}
    errors = errors or []

    for module in (
        "boardcomposer.solver.generators",
        "boardcomposer.solver.strategies",
        "boardcomposer.io.registry",
        "boardcomposer.export.registry",
    ):
        monkeypatch.setattr(
            f"{module}.discover_plugins", lambda group: (plugins, errors)
        )


def test_plugin_summary_with_no_plugins_installed(monkeypatch):
    _patch_all_groups(monkeypatch)

    summary = plugin_summary()

    assert set(summary) == {"generators", "strategies", "importers", "exporters"}
    for group in summary.values():
        assert group["installed"] == []
        assert group["errors"] == []


def test_plugin_summary_lists_installed_plugins_without_built_ins(monkeypatch):
    _patch_all_groups(monkeypatch, plugins={"custom": lambda *a, **k: None})

    summary = plugin_summary()

    assert summary["generators"]["installed"] == ["custom"]
    assert "horizontal" not in summary["generators"]["installed"]
    assert summary["strategies"]["installed"] == ["custom"]
    assert "balanced" not in summary["strategies"]["installed"]


def test_plugin_summary_surfaces_load_errors(monkeypatch):
    error = PluginLoadError(name="broken", error="boom")
    _patch_all_groups(monkeypatch, errors=[error])

    summary = plugin_summary()

    assert summary["generators"]["errors"] == [{"name": "broken", "error": "boom"}]
    assert summary["exporters"]["errors"] == [{"name": "broken", "error": "boom"}]
