FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    ROBOT_REPORTS_DIR=/app/robot-reports \
    SCREENSHOTS_DIR=/app/target/screenshots

WORKDIR /app

# 1) Install deps + gosu
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      curl \
      build-essential \
      python3-dev \
      libffi-dev \
      libssl-dev \
      gosu && \
    rm -rf /var/lib/apt/lists/*

# 2) Create robot user
RUN groupadd -r robot && \
    useradd --no-log-init -r -g robot robot

# 3) Install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4) Copy project, pre-create dirs & fix perms
COPY . .
RUN mkdir -p "$ROBOT_REPORTS_DIR" "$SCREENSHOTS_DIR" \
 && chown -R robot:robot /app \
 && chmod -R 0755 /app

# 5) Switch to robot
USER robot

# 6) Default command: run Robot into the pre-created dirs
ENTRYPOINT ["robot"]
CMD ["--outputdir", "/app/robot-reports", "--loglevel", "TRACE", "tests/"]