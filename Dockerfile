
FROM python:3-slim


ENV PYTHONDONTWRITEBYTECODE=1


ENV PYTHONUNBUFFERED=1


COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt  # --no-cache-dir zum Minimieren der Image-Größe

WORKDIR /app
COPY . /app


RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


CMD ["python", "NilsAbgabe.py"]
