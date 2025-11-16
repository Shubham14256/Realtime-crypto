from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import ccxt
from cachetools import TTLCache
import asyncio
import json
import logging
import time
from datetime import datetime, timezone
from typing import Set
from middleware import RateLimiter, PerformanceMonitor, CacheAnalytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Cryptocurrency Data Server (Advanced)",
    description="Production-ready cryptocurrency data with WebSocket, caching, rate limiting, and analytics",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize exchange
try:
    exchange = ccxt.binance()
    logger.info("Binance exchange initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize exchange: {e}")
    exchange = None

# Cache for prices and history (5-minute TTL)
cache = TTLCache(maxsize=100, ttl=300)

# Rate limiting and monitoring
rate_limiter = RateLimiter(requests_per_minute=100)
performance_monitor = PerformanceMonitor()
cache_analytics = CacheAnalytics()

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """
    Root endpoint - Returns server status and available resources.
    
    **Returns**: JSON object with server status message and API documentation link
    """
    return {
        "message": "MCP Crypto Server is running!",
        "version": "2.0.0",
        "status": "operational",
        "documentation": "http://127.0.0.1:8000/docs",
        "description": "Production-ready cryptocurrency data server with WebSocket, caching, and analytics"
    }


class CryptoAPIError(Exception):
    """Custom exception for cryptocurrency API errors"""
    pass


def validate_symbol(symbol: str) -> bool:
    """Validate symbol format"""
    if not symbol or "/" not in symbol:
        raise CryptoAPIError(f"Invalid symbol format: {symbol}. Expected format: BTC/USDT")
    return True


@app.get("/price/{symbol:path}")
async def get_price(symbol: str):
    """
    Get current price for a cryptocurrency symbol.
    
    - **symbol**: Trading pair symbol (e.g., BTC/USDT, ETH/USDT)
    - **Returns**: JSON object with symbol and current price
    """
    try:
        validate_symbol(symbol)
        
        # Check cache
        cache_key = f"price:{symbol}"
        if cache_key in cache:
            logger.info(f"Cache hit for {symbol}")
            cache_analytics.record_hit(saved_ms=200)
            return cache[cache_key]
        
        cache_analytics.record_miss()
        
        # Validate exchange is available
        if not exchange:
            raise CryptoAPIError("Exchange service unavailable")
        
        # Fetch from exchange
        ticker = exchange.fetch_ticker(symbol)
        result = {
            "symbol": symbol, 
            "price": ticker['last'],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "high": ticker.get('high'),
            "low": ticker.get('low'),
            "volume": ticker.get('baseVolume')
        }
        
        # Store in cache
        cache[cache_key] = result
        logger.info(f"Fetched price for {symbol}: {result['price']}")
        return result
        
    except CryptoAPIError as e:
        logger.warning(f"Validation error for {symbol}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except (ccxt.BadSymbol, ccxt.ExchangeError) as e:
        logger.warning(f"Invalid symbol: {symbol}")
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found on exchange")
    except ccxt.ExchangeNotAvailable as e:
        logger.error(f"Exchange unavailable: {e}")
        raise HTTPException(status_code=503, detail="Cryptocurrency exchange service temporarily unavailable")
    except ccxt.NetworkError as e:
        logger.error(f"Network error fetching {symbol}: {e}")
        raise HTTPException(status_code=502, detail="Network error connecting to exchange")
    except Exception as e:
        logger.error(f"Unexpected error fetching price for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/history/{symbol:path}")
async def get_history(symbol: str, days: int = 30):
    """
    Get historical OHLCV data for a cryptocurrency symbol.
    
    - **symbol**: Trading pair symbol (e.g., BTC/USDT, ETH/USDT)
    - **days**: Number of days of historical data (default: 30)
    - **Returns**: JSON list of OHLCV candles [timestamp, open, high, low, close, volume]
    """
    try:
        validate_symbol(symbol)
        
        if days < 1 or days > 365:
            raise CryptoAPIError("Days must be between 1 and 365")
        
        # Check cache
        cache_key = f"history:{symbol}:{days}"
        if cache_key in cache:
            logger.info(f"Cache hit for history {symbol}")
            return {"symbol": symbol, "data": cache[cache_key]}
        
        # Validate exchange is available
        if not exchange:
            raise CryptoAPIError("Exchange service unavailable")
        
        # Fetch from exchange
        data = exchange.fetch_ohlcv(symbol, '1d', limit=days)
        
        result = {
            "symbol": symbol,
            "data": data,
            "count": len(data),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Store in cache
        cache[cache_key] = data
        logger.info(f"Fetched {len(data)} candles for {symbol}")
        return result
        
    except CryptoAPIError as e:
        logger.warning(f"Validation error for {symbol}: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except (ccxt.BadSymbol, ccxt.ExchangeError) as e:
        logger.warning(f"Invalid symbol: {symbol}")
        raise HTTPException(status_code=404, detail=f"Symbol '{symbol}' not found on exchange")
    except ccxt.ExchangeNotAvailable as e:
        logger.error(f"Exchange unavailable: {e}")
        raise HTTPException(status_code=503, detail="Cryptocurrency exchange service temporarily unavailable")
    except ccxt.NetworkError as e:
        logger.error(f"Network error fetching {symbol}: {e}")
        raise HTTPException(status_code=502, detail="Network error connecting to exchange")
    except Exception as e:
        logger.error(f"Unexpected error fetching history for {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.websocket("/ws/updates/{symbol:path}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    WebSocket endpoint for real-time price updates.
    
    - **symbol**: Trading pair symbol to stream (e.g., BTC/USDT)
    - Sends price updates every 5 seconds
    - Automatically reconnects on errors
    """
    try:
        validate_symbol(symbol)
        await websocket.accept()
        active_connections.add(websocket)
        logger.info(f"WebSocket connected for {symbol}")
        
        while True:
            try:
                if not exchange:
                    await websocket.send_json({"error": "Exchange service unavailable"})
                    await asyncio.sleep(5)
                    continue
                
                # Fetch current price
                ticker = exchange.fetch_ticker(symbol)
                data = {
                    "type": "price_update",
                    "symbol": symbol,
                    "price": ticker['last'],
                    "high": ticker.get('high'),
                    "low": ticker.get('low'),
                    "volume": ticker.get('baseVolume'),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                
                await websocket.send_json(data)
                logger.debug(f"WebSocket sent update for {symbol}")
                
            except (ccxt.BadSymbol, ccxt.ExchangeError):
                try:
                    await websocket.send_json({
                        "type": "error",
                        "error": f"Invalid symbol: {symbol}"
                    })
                except RuntimeError:
                    pass
                break
            except ccxt.NetworkError as e:
                try:
                    await websocket.send_json({
                        "type": "error",
                        "error": f"Network error: {str(e)}"
                    })
                except RuntimeError:
                    pass
            except Exception as e:
                logger.error(f"Error in WebSocket for {symbol}: {e}")
                try:
                    await websocket.send_json({
                        "type": "error",
                        "error": f"Error fetching data: {str(e)}"
                    })
                except RuntimeError:
                    pass
            
            # Wait 5 seconds before next update
            await asyncio.sleep(5)
            
    except CryptoAPIError as e:
        try:
            await websocket.send_json({"error": str(e)})
        except RuntimeError:
            pass
        await websocket.close(code=1008, reason=str(e))
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for {symbol}")
        active_connections.discard(websocket)
    except Exception as e:
        logger.error(f"WebSocket error for {symbol}: {e}")
        active_connections.discard(websocket)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "exchange": "connected" if exchange else "disconnected",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/cache-stats")
async def cache_stats():
    """Get cache statistics"""
    return {
        "cache_size": len(cache),
        "max_size": cache.maxsize,
        "ttl": cache.ttl,
        "items": list(cache.keys())
    }


@app.get("/metrics")
async def get_metrics(endpoint: str = None):
    """Get performance metrics for all or specific endpoint"""
    metrics = performance_monitor.get_metrics(endpoint)
    return {
        "endpoint": endpoint,
        "metrics": metrics if endpoint else performance_monitor.endpoint_metrics,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/health-score")
async def health_score():
    """Get service health score"""
    score = performance_monitor.get_health_score()
    cache_stats = cache_analytics.get_stats()
    
    return {
        **score,
        "cache_analytics": cache_stats,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/analytics")
async def analytics():
    """Get comprehensive analytics"""
    return {
        "performance": performance_monitor.get_health_score(),
        "cache": cache_analytics.get_stats(),
        "endpoints": performance_monitor.endpoint_metrics,
        "active_connections": len(active_connections),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware to track performance and rate limiting"""
    
    # Rate limiting
    client_id = request.client.host if request.client else "unknown"
    allowed, rate_info = rate_limiter.is_allowed(client_id)
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded", **rate_info},
            headers={"Retry-After": str(rate_info.get("retry_after", 60))}
        )
    
    # Track performance
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000  # Convert to ms
    
    # Record metrics
    endpoint = request.url.path
    performance_monitor.record_request(endpoint, process_time, response.status_code)
    
    # Add headers
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-RateLimit-Limit"] = str(rate_info.get("limit", 100))
    response.headers["X-RateLimit-Remaining"] = str(rate_info.get("remaining", 100))
    
    return response
