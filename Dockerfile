FROM python:3.12-slim

LABEL maintainer="gauravgirase1996@gmail.com" \
      org.opencontainers.image.title="FastAPI Application" \
      org.opencontainers.image.description="Application performance monitoring" \
      org.opencontainers.image.version="1.0.0"

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY . .
# Create non-root user
RUN addgroup --system fastapi && adduser --system --group fastapi

RUN chown -R fastapi:fastapi /app

USER fastapi

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import socket; s=socket.socket(); s.connect(('localhost',8000))" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
