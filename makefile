PYTHON=python3
VENV=venv
REQ=requirements.txt

.PHONY: all install clean run tests

all: install run

install:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r $(REQ)

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

run:
	$(VENV)/bin/python src/main.py

tests:
	$(VENV)/bin/python -m unittest discover -s tests
	