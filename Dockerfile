# Use Python 3.13 slim (removes high CVEs)
FROM python:3.11-slim

# Upgrade pip
RUN pip install --upgrade pip

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential 
#unixodbc-dev curl && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set Poetry configuration
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

# Disable creation of virtual environments by Poetry
RUN poetry config virtualenvs.create false

# Set working directory
WORKDIR /app

# Copy project files
# Copy pyproject.toml and install dependencies first (for caching)
COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the entire application code
COPY . .

# Expose port
EXPOSE 8000

# Environment variables
ARG ENVIRONMENT=production
ENV ENVIRONMENT=${ENVIRONMENT}

# Default command to run FastAPI app
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]