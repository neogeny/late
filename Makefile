test: base lint pytest mypy


base:
	-@ pip install -qU pip


lint:
	-@ pip install -qU ruff
	ruff --preview late test

pytest:
	-@ pip install -qU pytest
	pytest -v


mypy:
	-@ pip install -qU mypy
	mypy --ignore-missing-imports --check-untyped-defs late test
