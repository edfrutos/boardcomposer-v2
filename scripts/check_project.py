import re
import tomllib
from pathlib import Path


REQUIRED_PATHS = [
    "pyproject.toml",
    "Makefile",
    "src/boardcomposer",
    "src/boardcomposer/domain",
    "src/boardcomposer/layout",
    "src/boardcomposer/solver",
    "src/boardcomposer/io",
    "tests",
    "data/samples/basic_boards.csv",
]

DEPLOY_SPEC = Path("studio/pysidedeploy.spec")


def _packaged_version() -> str | None:
    """The --macos-app-version Nuitka bakes into the .app bundle.

    Lives in an .ini-style file that has to be read as text: configparser
    chokes on the spec's duplicate `plugins` keys across sections.
    """
    if not DEPLOY_SPEC.exists():
        return None

    match = re.search(
        r"--macos-app-version=(\S+)", DEPLOY_SPEC.read_text(encoding="utf-8")
    )
    return match.group(1) if match else None


def _check_packaged_version_matches_pyproject() -> str | None:
    """The packaged version is what a user sees in Finder's Get Info, and
    what macOS compares when deciding whether an install is an upgrade. It
    sits in a different file from the real version, so nothing but this
    check stops the two from drifting apart release after release.
    """
    with Path("pyproject.toml").open("rb") as file:
        project_version = tomllib.load(file)["project"]["version"]

    packaged = _packaged_version()
    if packaged is None:
        return f"{DEPLOY_SPEC}: falta --macos-app-version en extra_args"

    if packaged != project_version:
        return (
            f"La versión empaquetada no coincide con la del proyecto: "
            f"{DEPLOY_SPEC} dice {packaged}, pyproject.toml dice "
            f"{project_version}"
        )

    return None


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not Path(path).exists()]

    if missing:
        print("Faltan rutas:")
        for path in missing:
            print(f"- {path}")
        raise SystemExit(1)

    error = _check_packaged_version_matches_pyproject()
    if error:
        raise SystemExit(error)

    print("BoardComposer OK")


if __name__ == "__main__":
    main()
