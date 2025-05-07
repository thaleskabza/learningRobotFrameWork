# learningRobotFrameWork
learningRobotFrameWork


# 
```bash
 python3 -m venv .venv;source .venv/bin/activate      
```
# 
```bash
docker-compose build --no-cache;docker-compose up -d;echo "🔍 Running Robot Framework tests…";mkdir -p "$ROBOT_REPORTS";docker-compose run --rm test-runner
```

# Linking Binary 'chromedriver' to '/opt/homebrew/bin/chromedriver'