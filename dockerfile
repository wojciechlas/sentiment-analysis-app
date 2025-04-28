# Dockerfile

# Stage 1: Install dependencies
# Use a minimal Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Set the working directory in the container
WORKDIR /app

# Copy only dependency files first (to leverage caching)
COPY pyproject.toml uv.lock ./

# Install the project's dependencies using the lockfile and settings
RUN uv sync --no-dev

# Stage 2: Build the application
FROM scratch

# Set the working directory
WORKDIR /app

# Copy installed dependencies from the first stage
COPY --from=base /app /app

# Then, add the rest of the project source code and install it
ADD . /app

# Expose the application port
EXPOSE 8000

# Run the application with uv
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]