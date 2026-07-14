from PySide6.QtWidgets import QApplication

import studio.app
from studio.main_window import MainWindow


def test_main_builds_and_shows_a_window_then_returns_the_exec_result(monkeypatch):
    # main() always constructs its own QApplication(sys.argv); Qt only allows
    # one instance per process, and other test modules in this suite already
    # create one. Reuse the existing singleton instead of the real
    # constructor so this test is safe to run alongside them in any order.
    app = QApplication.instance() or QApplication([])
    monkeypatch.setattr(studio.app, "QApplication", lambda argv: app)
    monkeypatch.setattr(QApplication, "exec", lambda self: 0)

    windows_before = QApplication.topLevelWidgets()

    exit_code = studio.app.main()

    assert exit_code == 0
    new_windows = [
        widget
        for widget in QApplication.topLevelWidgets()
        if widget not in windows_before and isinstance(widget, MainWindow)
    ]
    assert len(new_windows) == 1
    assert new_windows[0].isVisible()
