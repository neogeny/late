test: lint pytest mypy


lint:
	ruff late test

pytest:
	pytest -v


mypy:
	mypy --ignore-missing-imports --check-untyped-defs late test
