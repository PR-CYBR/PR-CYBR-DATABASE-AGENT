# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set application directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./requirements.txt
RUN if [ -s requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Copy application source
COPY src ./src

# Default command to run the agent
ENTRYPOINT ["python", "src/main.py"]
