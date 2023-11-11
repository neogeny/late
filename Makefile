test: pytest mypy

pytest:
	pytest -v


mypy:
	mypy --ignore-missing-imports --check-untyped-defs late test
