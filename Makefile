.PHONY: lint format typecheck coverage

lint:
	ruff check --fix .

format:
	ruff format .

typecheck:
	mypy src

coverage:
	pytest --cov-report=html