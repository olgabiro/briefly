import subprocess


def lint() -> None:
    subprocess.run(["ruff", "check", ".", "--fix"], check=True)


def format() -> None:
    subprocess.run(["ruff", "format", "."], check=True)


def typecheck() -> None:
    subprocess.run(["mypy", "--install-types", "src"], check=True)


def coverage() -> None:
    subprocess.run(["pytest", "--cov-report=html"])
