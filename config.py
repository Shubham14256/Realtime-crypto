# Configuration file for Cryptocurrency Data Server

# Server Configuration
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_RELOAD = True  # Auto-reload on code changes

# Logging Configuration
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Cache Configuration
CACHE_MAX_SIZE = 100  # Maximum number of cached items
CACHE_TTL = 300  # Cache time-to-live in seconds (5 minutes)

# Exchange Configuration
EXCHANGE = "binance"  # CCXT exchange name
EXCHANGE_TIMEOUT = 10000  # Milliseconds
ENABLE_RATE_LIMITER = True

# WebSocket Configuration
WEBSOCKET_UPDATE_INTERVAL = 5  # Seconds between price updates
MAX_WEBSOCKET_CONNECTIONS = 1000

# API Configuration
API_TITLE = "Cryptocurrency Data Server"
API_VERSION = "1.0.0"
DOCS_URL = "/docs"
REDOC_URL = "/redoc"

# Error Handling
HANDLE_INVALID_SYMBOLS = True
HANDLE_NETWORK_ERRORS = True
RETRY_ON_FAILURE = True
MAX_RETRIES = 3
RETRY_DELAY = 2  # Seconds

# Performance
ENABLE_CORS = True
CORS_ORIGINS = ["*"]  # Allow all origins. Restrict for production.
COMPRESSION_ENABLED = True
COMPRESSION_LEVEL = 6  # 1-9 compression level

# Monitoring
HEALTH_CHECK_ENABLED = True
CACHE_STATS_ENABLED = True
METRICS_ENABLED = False

# Security (for production)
REQUIRE_API_KEY = False
# API_KEY = "your-api-key-here"
# API_KEY_HEADER = "X-API-Key"
