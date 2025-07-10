# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.8.2 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set workdir
WORKDIR /app

# Copy pyproject and lock file first
COPY pyproject.toml poetry.lock* /app/

# Disable virtualenv creation
RUN poetry config virtualenvs.create false

# Install deps
RUN poetry install --no-interaction --no-ansi

# Copy rest of the code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app/streamlit_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
