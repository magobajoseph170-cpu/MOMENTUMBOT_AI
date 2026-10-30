FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY public_api/requirements.txt /app/public_api/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/public_api/requirements.txt
COPY public_api/__init__.py public_api/app.py /app/public_api/
USER 10001
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn public_api.app:app --host 0.0.0.0 --port ${PORT:-8000}"]
