# 🚀 QUICK COMMAND REFERENCE

This file contains all commands needed to run, test, and deploy the project.

---

## ⚡ Quick Start (5 minutes)

```bash
# 1. Navigate to project
cd "c:\historical cryptocurrency"

# 2. Activate virtual environment
.venv\Scripts\activate

# 3. Start server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. In another terminal, test endpoints
curl http://localhost:8000/price/BTC/USDT
curl http://localhost:8000/health

# 5. Visit API docs
# Open browser: http://localhost:8000/docs
```

---

## 🧪 Running Tests

```bash
# Navigate to project
cd "c:\historical cryptocurrency"

# Activate environment
.venv\Scripts\activate

# Run all tests with verbose output
python -m pytest test_main.py -v

# Run specific test
python -m pytest test_main.py::test_get_price_success -v

# Run tests with coverage
python -m pytest test_main.py --cov=main --cov-report=html

# Run tests with specific marker
python -m pytest test_main.py -m "not skip" -v

# Run tests and show print statements
python -m pytest test_main.py -v -s
```

**Expected Result**: `24 passed, 1 skipped in ~20 seconds`

---

## 🌐 API Endpoints

```bash
# Get current BTC/USDT price
curl http://localhost:8000/price/BTC/USDT

# Get price with metadata
curl http://localhost:8000/price/BTC/USDT?include_metadata=true

# Get 30 days of history
curl http://localhost:8000/history/BTC/USDT?days=30

# Get specific number of candles
curl http://localhost:8000/history/ETH/USDT?count=100

# Check service health
curl http://localhost:8000/health

# Get health score
curl http://localhost:8000/health-score

# View performance metrics
curl http://localhost:8000/metrics

# View cache statistics
curl http://localhost:8000/cache-stats

# View cache analytics
curl http://localhost:8000/analytics

# WebSocket (use JavaScript or websocat)
websocat ws://localhost:8000/ws/updates/BTC/USDT
```

---

## 🐳 Docker Commands

```bash
# Build Docker image
docker build -t crypto-server:latest .

# Run container
docker run -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  -e CACHE_TTL=300 \
  --name crypto-server \
  crypto-server:latest

# Run with docker-compose
docker-compose up -d

# View logs
docker logs -f crypto-server

# Stop container
docker stop crypto-server

# Remove container
docker rm crypto-server

# Remove image
docker rmi crypto-server:latest
```

---

## 📦 Setup & Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install with development dependencies
pip install -r requirements.txt[dev]

# Install package in development mode
pip install -e .

# Install specific version
pip install fastapi==0.104.1 ccxt==4.0.36
```

---

## 📊 Development Workflow

```bash
# Format code with black
black main.py test_main.py middleware.py

# Check code style with flake8
flake8 main.py --max-line-length=100

# Type checking with mypy
mypy main.py

# Check for security issues
bandit main.py

# Generate requirements from imports
pip freeze > requirements.txt

# Update requirements
pip install --upgrade -r requirements.txt
```

---

## 🔍 Debugging

```bash
# Start with debug logging
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" && \
  python -m uvicorn main:app --reload --log-level debug

# Run single test with debugging
python -m pytest test_main.py::test_get_price_success -v -s --pdb

# Print environment variables
python -c "import os; print(os.environ)"

# Check Python version
python --version

# Check installed packages
pip list

# Check specific package version
pip show fastapi
```

---

## 🚀 Deployment

### Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create crypto-data-server

# Deploy
git push heroku main

# View logs
heroku logs -t

# Set environment variables
heroku config:set LOG_LEVEL=INFO

# Open app
heroku open
```

### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ubuntu@instance-ip

# Install dependencies
sudo apt update && sudo apt install -y python3.11 python3.11-venv

# Clone and setup
git clone https://github.com/username/historical-cryptocurrency.git
cd historical-cryptocurrency
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run with systemd
sudo systemctl start crypto-server
sudo systemctl status crypto-server
sudo systemctl enable crypto-server
```

### Docker on Linux
```bash
# Pull and run
docker run -d -p 8000:8000 crypto-server:latest

# Use docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 📝 Git Commands

```bash
# Initialize repository
git init

# Add files
git add .

# Commit changes
git commit -m "feat: Add feature description"

# Add remote
git remote add origin https://github.com/username/repo.git

# Push to GitHub
git branch -M main
git push -u origin main

# Create feature branch
git checkout -b feature/feature-name

# Merge feature
git checkout main
git merge feature/feature-name

# Create tag
git tag v1.0.0

# Push tag
git push origin v1.0.0

# View commit history
git log --oneline
```

---

## 🔐 Environment Variables

```bash
# Create .env file
cat > .env << EOF
LOG_LEVEL=INFO
CACHE_TTL=300
EXCHANGE_TIMEOUT=10
MAX_CACHE_ITEMS=100
EOF

# Load from .env
from dotenv import load_dotenv
load_dotenv()
```

---

## 📊 Performance Testing

```bash
# Using Apache Bench (ab)
ab -n 1000 -c 50 http://localhost:8000/price/BTC/USDT

# Using wrk (requires installation)
wrk -t4 -c100 -d30s http://localhost:8000/price/BTC/USDT

# Using Python requests
python -c "
import requests
import time
start = time.time()
for i in range(100):
    requests.get('http://localhost:8000/price/BTC/USDT')
print(f'100 requests: {time.time() - start:.2f}s')
"

# Using locust (load testing)
locust -f locustfile.py --host=http://localhost:8000
```

---

## 🧹 Cleanup Commands

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove test cache
rm -rf .pytest_cache

# Remove virtual environment
rm -rf .venv

# Clear pip cache
pip cache purge

# Remove all development files
rm -rf .eggs *.egg-info dist build

# Clean Docker
docker system prune -a
docker image prune -a
docker container prune
```

---

## 📚 Documentation Commands

```bash
# Generate documentation
pydoc -w main
pydoc -w middleware

# Generate API docs
pip install pdoc
pdoc main --output-directory docs

# Generate coverage report
coverage run -m pytest test_main.py
coverage report
coverage html
```

---

## 🆘 Troubleshooting Commands

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i :8000)

# Check network connectivity
ping google.com
curl https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT

# Test cryptocurrency API
python -c "
import ccxt
exchange = ccxt.binance()
print(exchange.fetch_ticker('BTC/USDT'))
"

# Check Python paths
python -c "import sys; print(sys.path)"

# Verify package installation
python -c "import fastapi; print(fastapi.__version__)"

# Test async functionality
python -c "
import asyncio
async def test():
    return 'async works'
print(asyncio.run(test()))
"
```

---

## 📋 Common Task Checklist

```bash
# Complete development cycle
git add .
git commit -m "feat: your message"
pytest test_main.py -v                    # Run tests
python -m uvicorn main:app --reload       # Test locally
docker build -t app:latest .              # Build Docker
docker run -p 8000:8000 app:latest        # Test Docker
git push origin main                       # Push to GitHub
```

---

## 🔗 Useful Links

- FastAPI Docs: https://fastapi.tiangolo.com
- CCXT Docs: https://docs.ccxt.com
- pytest Docs: https://docs.pytest.org
- Docker Docs: https://docs.docker.com
- Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
- AWS CLI: https://aws.amazon.com/cli/

---

## 🎯 Command Template (Copy & Paste Ready)

```bash
# Full development workflow
cd "c:\historical cryptocurrency"
.venv\Scripts\activate
pytest test_main.py -v
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

**Last Updated**: November 16, 2025  
**Version**: 1.0
