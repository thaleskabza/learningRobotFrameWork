# Dockerfile
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    ROBOT_REPORTS_DIR=/app/robot-reports \
    SCREENSHOTS_DIR=/app/target/screenshots

WORKDIR /app

# Install OS deps, dev headers & cleanup
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      build-essential \
      python3-dev \
      libffi-dev \
      libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r robot && \
    useradd --no-log-init -r -g robot robot

# Copy & install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project & prepare output dirs
COPY . .
RUN mkdir -p "$ROBOT_REPORTS_DIR" "$SCREENSHOTS_DIR" \
 && chown -R robot:robot /app \
 && chmod -R 0777 "$ROBOT_REPORTS_DIR" "$SCREENSHOTS_DIR"

USER robot

# Run Robot Framework by default; args can be overridden in docker-compose
ENTRYPOINT ["robot"]
CMD ["--outputdir", "/app/robot-reports", "--loglevel", "TRACE", "tests/"]
