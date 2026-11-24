VENV := .venv
PY := $(VENV)/bin/python

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	touch $(VENV)/bin/activate

.PHONY: venv test clean

venv: $(VENV)/bin/activate

test: venv
	$(PY) -m unittest test -v

clean:
	rm -rf $(VENV)