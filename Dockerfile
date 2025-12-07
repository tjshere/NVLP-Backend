# Build stage: Install dependencies that require compilation
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies to a local directory
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Runtime stage: Clean image with only runtime files
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV PATH=/root/.local/bin:$PATH

# Set work directory
WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /root/.local /root/.local

# Copy project files
COPY . .

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput || true

# Expose the port
EXPOSE $PORT

# Run gunicorn
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

