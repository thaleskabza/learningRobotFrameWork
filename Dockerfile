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

# 4) Copy entrypoint helper
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 5) Copy rest of project (tests, resources, etc.)
COPY . .

# 6) Switch to our entrypoint (which will drop to robot for us)
ENTRYPOINT ["/entrypoint.sh"]
CMD ["--outputdir", "/app/robot-reports", "--loglevel", "TRACE", "tests/"]
