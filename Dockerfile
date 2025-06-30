# Use Python 3.13 slim image (latest stable)
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files (this will run during build)
RUN python manage.py collectstatic --noinput --clear

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Expose port
EXPOSE 8881

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8881/health/', timeout=10)" || exit 1

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8881", "--workers", "3", "--timeout", "120", "simbin.wsgi:application"]
