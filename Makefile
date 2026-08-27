PYTHON := .venv/bin/python
PYTEST := .venv/bin/pytest
RUFF := .venv/bin/ruff
BOARDCOMPOSER := .venv/bin/boardcomposer
BOARDCOMPOSER_STUDIO := .venv/bin/boardcomposer-studio
GUNICORN := .venv/bin/gunicorn
PYSIDE6_DEPLOY := .venv/bin/pyside6-deploy

.PHONY: test run studio demo json status check check-deploy lint format serve package

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

# Comprueba que la API desplegada en la VPS sirve la versión actual
# (DT-0034/DT-0035). Necesita BC_DEPLOY_AUTH="usuario:contraseña" del HTTP
# Basic de nginx; BC_DEPLOY_API_URL si no es bc.efjdefrutos.com.
check-deploy:
	$(PYTHON) scripts/check_deployment.py

lint:
	$(RUFF) check .

format:
	$(RUFF) format .

serve:
	$(GUNICORN) --bind 0.0.0.0:5050 "boardcomposer.api:create_app()"

package:
	cd studio && ../$(PYSIDE6_DEPLOY) -f app.py
