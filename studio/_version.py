"""Single source of truth for the running Studio version, readable both
from source and from inside a frozen Nuitka .app (unlike
importlib.metadata, which needs installed dist-info that a onefile build
doesn't carry). Kept in sync with pyproject.toml by scripts/check_project.py,
same guard pattern already used for studio/pysidedeploy.spec.
"""

__version__ = "0.3.24"
