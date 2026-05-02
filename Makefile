.PHONY: help install run test all clean

PYTHON ?= python3
PIP    ?= $(PYTHON) -m pip
NB     := adc.ipynb

help:
	@echo "Attendance Decay Curve — Makefile targets"
	@echo "  make install  - Install Python dependencies from requirements.txt"
	@echo "  make run      - Execute the notebook end-to-end (in place)"
	@echo "  make test     - Run the test suite"
	@echo "  make all      - Install dependencies and execute the notebook"
	@echo "  make clean    - Remove caches and notebook checkpoints"

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m jupyter nbconvert --to notebook --execute --inplace $(NB)

test:
	$(PYTHON) -m pytest tests/

all: install run

clean:
	find . -type d -name __pycache__       -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
	find . -type d -name .pytest_cache     -exec rm -rf {} +
