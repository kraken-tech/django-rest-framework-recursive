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


@nox.session()
@nox.parametrize(
    "drf_version",
    [
        nox.param("djangorestframework>=3.13,<3.14", id="drf=3.13"),
        nox.param("djangorestframework>=3.14,<3.15", id="drf=3.14"),
        nox.param("djangorestframework>=3.15,<3.16", id="drf=3.15"),
    ],
)
@nox.parametrize(
    "django_version",
    [
        nox.param("django>=3.2,django<3.3", id="django=3.2.X"),
        nox.param("django>=4.0,django<4.1", id="django=4.0.X"),
        nox.param("django>=4.1,django<4.2", id="django=4.1.X"),
        nox.param("django>=4.2,django<4.3", id="django=4.2.X"),
    ],
)
@nox.parametrize(
    "python",
    [
        nox.param("3.10", id="python3.10"),
    ],
)
def tests(session: nox.Session, django_version: str, drf_version: str) -> None:
    """
    Run the test suite.
    """
    with temp_constraints_file() as constraints_file, temp_lock_file() as lock_file:
        # Create a constraints file with the parameterized package versions.
        # It's easy to add more constraints here if needed.
        constraints_file.write(f"{django_version}\n")
        constraints_file.write(f"{drf_version}\n")

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

    session.run(*commands, *session.posargs)
