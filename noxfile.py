"""Nox sessions."""

import sys

import nox
from nox_poetry import Session, session

locations = "dcat_ap_no_validator_service", "tests", "noxfile.py"
nox.options.stop_on_first_error = True
nox.options.sessions = (
    "lint",
    "mypy",
    "unit_tests",
    "integration_tests",
    "contract_tests",
)


@session(python=["3.10"])
def unit_tests(session: Session) -> None:
    """Run the unit test suite."""
    args = session.posargs
    session.install(".")
    session.install(
        "requests",
        "pytest",
        "pytest-mock",
        "pytest-aiohttp",
        "pytest-profiling",
        "aioresponses",
    )
    session.run(
        "pytest",
        "-m unit",
        "-rfE",
        *args,
        env={"CONFIG": "test"},
    )


@session(python=["3.10"])
def integration_tests(session: Session) -> None:
    """Run the integration test suite."""
    args = session.posargs or ["--cov"]
    session.install(".")
    session.install(
        "coverage[toml]",
        "requests",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "pytest-aiohttp",
        "pytest-profiling",
        "aioresponses",
    )
    session.run(
        "pytest",
        "-m integration",
        "-rfE",
        *args,
        env={"CONFIG": "test"},
    )


@session(python=["3.10"])
def contract_tests(session: Session) -> None:
    """Run the contract test suite."""
    args = session.posargs
    session.install(".")
    session.install(
        "requests",
        "pytest",
        "pytest-docker",
        "pytest_mock",
        "pytest-asyncio",
        "aioresponses",
    )
    session.run(
        "pytest",
        "-m contract",
        "-rfE",
        *args,
        env={
            "REDIS_HOST": "redis",
            "REDIS_PASSWORD": "secret",
            "CONFIG": "production",
            "TIMEOUT": "0",
            "LOGGING_LEVEL": "DEBUG",
        },
    )


@session(python=["3.10"])
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


@session(python=["3.10"])
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    session.install(
        "flake8",
        "flake8-annotations",
        "flake8-bandit",
        "flake8-black",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-import-order",
        "pep8-naming",
    )
    session.run("flake8", *args)


@session(python=["3.10"])
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or [
        "--install-types",
        "--non-interactive",
        "dcat_ap_no_validator_service",
        "tests",
    ]
    session.install(".")
    session.install("mypy", "pytest")
    session.run("mypy", *args)
    if not session.posargs:
        session.run("mypy", f"--python-executable={sys.executable}", "noxfile.py")


@session(python=["3.10"])
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.install("coverage[toml]")
    session.run("coverage", "xml", "--fail-under=0")
