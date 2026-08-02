"""Human-readable session labels for candidate solutions (IDE-0027).

Pure function, no Qt dependency — replaces the raw list index ("Solución 1",
"Solución 2"...) that the Comparador and MainWindow used to show, which
changes meaning every time a comparison is regenerated.
"""

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def solution_label(index: int) -> str:
    if index < 0:
        raise ValueError("index debe ser >= 0")

    if index < len(_LETTERS):
        return _LETTERS[index]

    return str(index + 1)
