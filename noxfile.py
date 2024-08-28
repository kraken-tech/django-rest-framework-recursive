"""
This `noxfile.py` is configured to run the test suite with multiple versions of Python and multiple
versions of Django (used as an example).
"""

import contextlib
import os
import tempfile
from typing import IO, Generator

import nox


# Use uv to manage venvs.
nox.options.default_venv_backend = "uv"


@contextlib.contextmanager
def temp_constraints_file() -> Generator[IO[str], None, None]:
    with tempfile.NamedTemporaryFile(mode="w", prefix="constraints.", suffix=".txt") as f:
        yield f


@contextlib.contextmanager
def temp_lock_file() -> Generator[IO[str], None, None]:
    with tempfile.NamedTemporaryFile(mode="w", prefix="packages.", suffix=".txt") as f:
        yield f


valid_version_combinations = [
    # Python 3.10
    ("3.10", "django>=3.2,<3.3", "djangorestframework>=3.12,<3.13"),
    ("3.10", "django>=3.2,<3.3", "djangorestframework>=3.13,<3.14"),
    ("3.10", "django>=3.2,<3.3", "djangorestframework>=3.14,<3.15"),
    ("3.10", "django>=4.0,<4.1", "djangorestframework>=3.13,<3.14"),
    ("3.10", "django>=4.0,<4.1", "djangorestframework>=3.14,<3.15"),
    ("3.10", "django>=4.1,<4.2", "djangorestframework>=3.14,<3.15"),
    ("3.10", "django>=4.2,<4.3", "djangorestframework>=3.14,<3.15"),
    ("3.10", "django>=4.2,<4.3", "djangorestframework>=3.15,<3.16"),
    # Python 3.11
    ("3.11", "django>=4.1,<4.2", "djangorestframework>=3.14,<3.15"),
    ("3.11", "django>=4.1,<4.2", "djangorestframework>=3.15,<3.16"),
    ("3.11", "django>=4.2,<4.3", "djangorestframework>=3.14,<3.15"),
    ("3.11", "django>=4.2,<4.3", "djangorestframework>=3.15,<3.16"),
    ("3.11", "django>=5.0,<5.1", "djangorestframework>=3.14,<3.15"),
    ("3.11", "django>=5.0,<5.1", "djangorestframework>=3.15,<3.16"),
]


@nox.session()
@nox.parametrize("python, django_version, drf_version", valid_version_combinations)
def tests(session: nox.Session, django_version: str, drf_version: str) -> None:
    """
    Run the test suite.
    """
    with temp_constraints_file() as constraints_file, temp_lock_file() as lock_file:
        # Create a constraints file with the parameterized package versions.
        # It's easy to add more constraints here if needed.
        constraints_file.write(f"{django_version}\n")
        constraints_file.write(f"{drf_version}\n")
        constraints_file.write("pytest-django>=4.7.0\n")
        constraints_file.write("pytest>=8.3.2\n")
        constraints_file.flush()

        # Compile a new development lock file with the additional package constraints from this
        # session. Use a unique lock file name to avoid session pollution.
        session.run(
            "uv",
            "pip",
            "compile",
            "--quiet",
            "--strip-extras",
            "--extra=dev",
            "pyproject.toml",
            "--constraint",
            constraints_file.name,
            "--output-file",
            lock_file.name,
        )

        # Install the dependencies from the newly compiled lockfile and main package.
        session.install("-r", lock_file.name, ".")

    # When run in CircleCI, create JUnit XML test results.
    commands = ["pytest"]
    if "CIRCLECI" in os.environ:
        commands.append(f"--junitxml=test-results/junit.{session.name}.xml")

    session.run(
        *commands,
        *session.posargs,
    )
