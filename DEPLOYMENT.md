# Deployment Guide

This guide covers deploying the Cryptocurrency Data Server to various cloud platforms and on-premise environments.

## Table of Contents

1. [Local Development](#local-development)
2. [Docker Containerization](#docker-containerization)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
5. [AWS EC2](#aws-ec2)
6. [DigitalOcean](#digitalocean)
7. [Azure App Service](#azure-app-service)
8. [Production Best Practices](#production-best-practices)

## Local Development

### Prerequisites

- Python 3.8+
- pip and virtualenv
- Git

### Setup Steps

```bash
# Clone repository
git clone https://github.com/yourusername/historical-cryptocurrency.git
cd historical-cryptocurrency

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will be accessible at `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

## Docker Containerization

### Prerequisites

- Docker installed
- Docker Hub account (for pushing images)

### Dockerfile

Create `Dockerfile` in project root:

```dockerfile
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run Docker Image

```bash
# Build image
docker build -t crypto-data-server:latest .

# Run container
docker run -p 8000:8000 \
  -e LOG_LEVEL=INFO \
  -e CACHE_TTL=300 \
  --name crypto-server \
  crypto-data-server:latest

# View logs
docker logs -f crypto-server

# Stop container
docker stop crypto-server
```

### Docker Compose

Create `docker-compose.yml` for multi-container setup:

```yaml
version: '3.8'

services:
  crypto-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      LOG_LEVEL: INFO
      CACHE_TTL: 300
      EXCHANGE_TIMEOUT: 10
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 5s
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - crypto-server
```

Run with: `docker-compose up -d`

## Heroku Deployment

### Prerequisites

- Heroku account
- Heroku CLI installed
- Git installed

### Step 1: Prepare Application

Create `Procfile` (no extension):

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Create `runtime.txt`:

```
python-3.11.0
```

### Step 2: Deploy

```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create crypto-data-server

# Set environment variables
heroku config:set LOG_LEVEL=INFO
heroku config:set CACHE_TTL=300
heroku config:set EXCHANGE_TIMEOUT=10

# Deploy to Heroku
git push heroku main

# View logs
heroku logs -t

# Check app status
heroku open
```

### Step 3: Scale Dynos

```bash
# Scale to multiple workers
heroku ps:scale web=2

# View running processes
heroku ps

# Upgrade dyno type
heroku dyno:type upgrade web
```

### Monitoring

```bash
# Check app performance
heroku metrics

# Create alerts
heroku addons:create papertrail
heroku addons:create sendgrid
```

## AWS Elastic Beanstalk

### Prerequisites

- AWS account with Elastic Beanstalk access
- AWS CLI installed and configured
- EB CLI installed

### Step 1: Initialize EB Application

```bash
# Install EB CLI
pip install awseb-cli

# Initialize application
eb init -p python-3.11 crypto-data-server --region us-east-1

# Create environment
eb create crypto-env --instance-type t3.micro

# Deploy application
eb deploy

# Monitor logs
eb logs
```

### Step 2: Configure Application

Create `.ebextensions/01_app.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
    LOG_LEVEL: INFO
    CACHE_TTL: 300
  aws:elasticbeanstalk:container:python:
    WSGIPath: main:app
    NumProcesses: 3
    NumThreads: 15
  aws:autoscaling:asg:
    MinSize: 2
    MaxSize: 5
```

### Step 3: Monitor and Scale

```bash
# View environment health
eb health

# Scale environment
eb scale 3  # Scale to 3 instances

# Update environment
eb setenv LOG_LEVEL=DEBUG

# SSH into instance
eb ssh
```

## AWS EC2

### Prerequisites

- AWS account
- EC2 instance (Ubuntu 22.04 LTS recommended)
- Security groups configured for ports 80, 443, 8000

### Step 1: Launch EC2 Instance

```bash
# In AWS Console:
# 1. Launch t3.micro Ubuntu 22.04 LTS instance
# 2. Create security group allowing:
#    - Port 22 (SSH) from your IP
#    - Port 80 (HTTP) from 0.0.0.0/0
#    - Port 443 (HTTPS) from 0.0.0.0/0
# 3. Create key pair and download .pem file
```

### Step 2: Connect and Setup

```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install Git
sudo apt install -y git

# Clone repository
git clone https://github.com/yourusername/historical-cryptocurrency.git
cd historical-cryptocurrency

# Setup virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 3: Setup Systemd Service

Create `/etc/systemd/system/crypto-server.service`:

```ini
[Unit]
Description=Cryptocurrency Data Server
After=network.target

[Service]
Type=notify
User=ubuntu
WorkingDirectory=/home/ubuntu/historical-cryptocurrency
Environment="PATH=/home/ubuntu/historical-cryptocurrency/venv/bin"
ExecStart=/home/ubuntu/historical-cryptocurrency/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable crypto-server
sudo systemctl start crypto-server

# Check status
sudo systemctl status crypto-server

# View logs
sudo journalctl -u crypto-server -f
```

### Step 4: Setup Nginx Reverse Proxy

```bash
sudo apt install -y nginx

# Configure Nginx at /etc/nginx/sites-available/crypto-server
sudo tee /etc/nginx/sites-available/crypto-server > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/crypto-server /etc/nginx/sites-enabled/

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: Setup SSL with Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal check
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## DigitalOcean

### Prerequisites

- DigitalOcean account
- Droplet (Ubuntu 22.04 LTS recommended)
- doctl CLI (optional)

### Step 1: Create Droplet

```bash
# Using doctl CLI
doctl compute droplet create crypto-server \
  --region nyc3 \
  --image ubuntu-22-04-x64 \
  --size s-1vcpu-1gb \
  --enable-monitoring \
  --enable-backups
```

### Step 2: Setup Application

```bash
# SSH into droplet
ssh root@your_droplet_ip

# Follow EC2 setup steps above (Steps 2-5)
```

## Azure App Service

### Prerequisites

- Azure account
- Azure CLI installed
- Visual Studio Code with Azure extension (optional)

### Step 1: Create App Service

```bash
# Login to Azure
az login

# Create resource group
az group create --name crypto-rg --location eastus

# Create App Service Plan
az appservice plan create --name crypto-plan \
  --resource-group crypto-rg \
  --sku B1 \
  --is-linux

# Create Web App
az webapp create --resource-group crypto-rg \
  --plan crypto-plan \
  --name crypto-data-server \
  --runtime "python|3.11"
```

### Step 2: Deploy Application

```bash
# Create deployment user
az webapp deployment user set --user-name <username> --password <password>

# Configure local Git deployment
az webapp deployment source config-local-git \
  --name crypto-data-server \
  --resource-group crypto-rg

# Add Azure remote to Git
git remote add azure https://<username>@crypto-data-server.scm.azurewebsites.net/crypto-data-server.git

# Deploy
git push azure main
```

### Step 3: Configure Application Settings

```bash
# Set environment variables
az webapp config appsettings set --name crypto-data-server \
  --resource-group crypto-rg \
  --settings LOG_LEVEL=INFO CACHE_TTL=300

# Configure startup command
az webapp config set --name crypto-data-server \
  --resource-group crypto-rg \
  --startup-file "python -m uvicorn main:app --host 0.0.0.0 --port 8000"
```

## Production Best Practices

### 1. Security

```python
# Use environment variables for secrets
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

# Enable CORS only for trusted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

### 2. Monitoring and Logging

```bash
# Use structured logging
pip install python-json-logger

# Configure centralized logging
# - Datadog
# - New Relic
# - ELK Stack
# - CloudWatch (AWS)
# - Application Insights (Azure)
```

### 3. Performance Optimization

- **Enable caching**: Use Redis for distributed caching
- **Database optimization**: Connection pooling, query optimization
- **CDN**: CloudFront (AWS), Azure CDN, or Cloudflare
- **Load balancing**: Distribute traffic across multiple instances

### 4. Health Checks and Monitoring

```bash
# Configure health checks
# - Check `/health` endpoint regularly
# - Monitor cache hit rates
# - Monitor response times
# - Set up alerts for errors
```

### 5. Backup and Disaster Recovery

```bash
# Backup configuration
- Daily snapshots of server state
- Version control for all code
- Database backups (if applicable)
- Disaster recovery plan (RTO/RPO targets)
```

### 6. Rate Limiting and DDoS Protection

- Built-in rate limiter: 100 requests/minute per client
- Consider: WAF (Web Application Firewall)
- CloudFlare or AWS Shield for DDoS protection

### 7. Cost Optimization

| Platform | Small | Medium | Large |
|----------|-------|--------|-------|
| Heroku | $25/mo | $100/mo | $500/mo |
| AWS EC2 | $10/mo | $50/mo | $200/mo |
| DigitalOcean | $6/mo | $25/mo | $100/mo |
| Azure | $15/mo | $75/mo | $300/mo |

---

For questions or issues, refer to the [README.md](README.md) or open an issue on GitHub.
