FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies (curl for healthchecks, build essentials for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (tests, scripts, etc.)
COPY tests/ ./tests/
COPY robotframework/ ./robotframework/ 
# Assuming a directory for shared keywords/resources

# Create directories for reports and screenshots
RUN mkdir -p /app/robot-reports /app/target/screenshots

# Default command: run Robot Framework tests
CMD ["robot", "--outputdir", "robot-reports", "--loglevel", "TRACE", "tests/"]