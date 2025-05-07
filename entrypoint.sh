# entrypoint.sh
#!/bin/sh
set -e

# Ensure the runtime dirs exist and are owned by robot
mkdir -p "$ROBOT_REPORTS_DIR" "$SCREENSHOTS_DIR"
chown -R robot:robot "$ROBOT_REPORTS_DIR" "$SCREENSHOTS_DIR" /app

# Drop privileges and launch robot
exec gosu robot robot "$@"
