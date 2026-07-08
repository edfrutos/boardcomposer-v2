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


def main() -> None:
    missing = [path for path in REQUIRED_PATHS if not Path(path).exists()]

    if missing:
        print("Faltan rutas:")
        for path in missing:
            print(f"- {path}")
        raise SystemExit(1)

    print("BoardComposer OK")


if __name__ == "__main__":
    main()
