.PHONY: help install run test all clean

PYTHON ?= python3
VENV   := .venv
VPY    := $(VENV)/bin/python
VPIP   := $(VENV)/bin/pip
NB     := adc.ipynb

help:
	@echo "Attendance Decay Curve — Makefile targets"
	@echo "  make install  - Create .venv and install Python dependencies"
	@echo "  make run      - Execute the notebook end-to-end (in place)"
	@echo "  make test     - Run the test suite"
	@echo "  make all      - Install dependencies and execute the notebook"
	@echo "  make clean    - Remove caches and notebook checkpoints"

# Create the virtualenv only if it does not already exist.
$(VPY):
	$(PYTHON) -m venv $(VENV)
	$(VPIP) install --upgrade pip

install: $(VPY)
	$(VPIP) install -r requirements.txt

run: install
	$(VPY) -m jupyter nbconvert --to notebook --execute --inplace $(NB)

test: install
	$(VPY) -m pytest tests/

all: install run

clean:
	find . -type d -name __pycache__        -exec rm -rf {} +
	find . -type d -name .ipynb_checkpoints -exec rm -rf {} +
	find . -type d -name .pytest_cache      -exec rm -rf {} +
