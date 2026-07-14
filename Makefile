PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff
BOARDCOMPOSER := .venv/bin/boardcomposer
BOARDCOMPOSER_STUDIO := .venv/bin/boardcomposer-studio
GUNICORN := .venv/bin/gunicorn
PYSIDE6_DEPLOY := .venv/bin/pyside6-deploy

.PHONY: test run studio demo json status check lint format serve package

test:
	$(PYTEST)

run:
	$(BOARDCOMPOSER)

studio:
	$(BOARDCOMPOSER_STUDIO)

demo:
	$(BOARDCOMPOSER) --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600

json:
	$(BOARDCOMPOSER) --csv data/samples/basic_boards.csv --max-length 3000 --max-width 600 --json

status:
	git status

check:
	$(PYTHON) scripts/check_project.py
	$(RUFF) check .
	$(PYTEST)

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

serve:
	$(GUNICORN) --bind 0.0.0.0:5050 "boardcomposer.api:create_app()"

package:
	cd studio && ../$(PYSIDE6_DEPLOY) -f app.py
