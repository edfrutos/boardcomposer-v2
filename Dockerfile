# API HTTP de BoardComposer (IDE-0014). No incluye BoardComposer Studio
# (aplicación de escritorio PySide6) — fuera de alcance de un despliegue Cloud.
FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY src/ src/
COPY studio/ studio/

RUN pip install --no-cache-dir ".[prod]"

RUN useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5050

# BOARDCOMPOSER_API_KEY y ANTHROPIC_API_KEY se inyectan en tiempo de
# despliegue (ver docs/deploy.md) — sin valor por defecto aquí a propósito.
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "boardcomposer.api:create_app()"]
