# Contact360 DocsAI Admin — Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV DJANGO_ENV=production

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Deploy checks (production settings); build-time secrets are placeholders only
RUN SECRET_KEY="docker-build-placeholder-secret-key-32chars!!" ALLOWED_HOSTS=localhost,127.0.0.1 \
    python manage.py check --deploy

# Collect static files
RUN SECRET_KEY="docker-build-placeholder-secret-key-32chars!!" ALLOWED_HOSTS=localhost,127.0.0.1 \
    python manage.py collectstatic --noinput

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "docsai.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
