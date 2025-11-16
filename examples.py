"""
Usage Examples for Cryptocurrency Data Server

This file contains practical examples for using the cryptocurrency data server
in different scenarios.
"""

# ============= PYTHON EXAMPLES =============

import requests
import asyncio
import json
from typing import List, Dict

# Example 1: Fetch Current Price
def get_current_price(symbol: str) -> Dict:
    """Get the current price for a cryptocurrency symbol."""
    url = f"http://127.0.0.1:8000/price/{symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.json()}")
        return None


def example_get_price():
    """Example: Get current Bitcoin price"""
    price_data = get_current_price("BTC/USDT")
    if price_data:
        print(f"Bitcoin Price: ${price_data['price']}")
        print(f"24h High: ${price_data['high']}")
        print(f"24h Low: ${price_data['low']}")
        print(f"24h Volume: {price_data['volume']} BTC")


# Example 2: Fetch Historical Data
def get_historical_data(symbol: str, days: int = 30) -> List:
    """Get historical OHLCV data for a symbol."""
    url = f"http://127.0.0.1:8000/history/{symbol}"
    params = {"days": days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error: {response.status_code}")
        return []


def example_get_history():
    """Example: Get 7 days of Bitcoin data"""
    data = get_historical_data("BTC/USDT", days=7)
    for candle in data:
        timestamp, open_price, high, low, close, volume = candle
        print(f"Open: ${open_price} | High: ${high} | Low: ${low} | Close: ${close}")


# Example 3: Batch Price Requests
def get_multiple_prices(symbols: List[str]) -> Dict[str, float]:
    """Get prices for multiple symbols."""
    prices = {}
    for symbol in symbols:
        price_data = get_current_price(symbol)
        if price_data:
            prices[symbol] = price_data["price"]
    return prices


def example_batch_prices():
    """Example: Get prices for multiple cryptocurrencies"""
    symbols = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "XRP/USDT", "SOL/USDT"]
    prices = get_multiple_prices(symbols)
    for symbol, price in prices.items():
        print(f"{symbol}: ${price:.2f}")


# Example 4: Price Comparison
def compare_prices(symbol: str) -> Dict:
    """Get current price and compare with historical data."""
    current = get_current_price(symbol)
    history = get_historical_data(symbol, days=30)
    
    if not current or not history:
        return {}
    
    prices = [candle[4] for candle in history]  # close prices
    avg_30d = sum(prices) / len(prices)
    min_30d = min(prices)
    max_30d = max(prices)
    
    return {
        "symbol": symbol,
        "current_price": current["price"],
        "30d_average": avg_30d,
        "30d_high": max_30d,
        "30d_low": min_30d,
        "change_from_avg": ((current["price"] - avg_30d) / avg_30d) * 100
    }


def example_price_comparison():
    """Example: Analyze Bitcoin price against 30-day average"""
    analysis = compare_prices("BTC/USDT")
    print(f"Current Price: ${analysis['current_price']:.2f}")
    print(f"30-Day Average: ${analysis['30d_average']:.2f}")
    print(f"30-Day Range: ${analysis['30d_low']:.2f} - ${analysis['30d_high']:.2f}")
    print(f"Change from Average: {analysis['change_from_avg']:.2f}%")


# Example 5: WebSocket Streaming (Python)
import asyncio
import websockets
import json


async def stream_prices(symbol: str, duration_seconds: int = 60):
    """Stream real-time price updates via WebSocket."""
    url = f"ws://127.0.0.1:8000/ws/updates/{symbol}"
    start_time = asyncio.get_event_loop().time()
    
    async with websockets.connect(url) as websocket:
        while asyncio.get_event_loop().time() - start_time < duration_seconds:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data.get("type") == "price_update":
                    print(f"{data['symbol']} - Price: ${data['price']} | Time: {data['timestamp']}")
                elif data.get("type") == "error":
                    print(f"Error: {data['error']}")
                    break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break


async def example_websocket_stream():
    """Example: Stream Bitcoin prices for 30 seconds"""
    print("Starting WebSocket stream (30 seconds)...")
    await stream_prices("BTC/USDT", duration_seconds=30)
    print("Stream ended")


# Example 6: Real-time Price Alert
async def price_alert(symbol: str, target_price: float):
    """Alert when price reaches target."""
    url = f"ws://127.0.0.1:8000/ws/updates/{symbol}"
    
    async with websockets.connect(url) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data.get("type") == "price_update":
                    current_price = data["price"]
                    
                    if current_price >= target_price:
                        print(f"🔔 ALERT! {symbol} reached ${current_price} (target: ${target_price})")
                        break
                    else:
                        print(f"{symbol}: ${current_price} (target: ${target_price})")
            except Exception as e:
                print(f"Error: {e}")
                break


async def example_price_alert():
    """Example: Alert when Bitcoin reaches $100,000"""
    await price_alert("BTC/USDT", target_price=100000)


# Example 7: Technical Analysis (Simple Moving Average)
def calculate_sma(symbol: str, period: int = 20) -> float:
    """Calculate Simple Moving Average."""
    data = get_historical_data(symbol, days=period + 10)
    if not data or len(data) < period:
        return None
    
    close_prices = [candle[4] for candle in data[-period:]]
    sma = sum(close_prices) / period
    return sma


def example_sma():
    """Example: Calculate 20-day SMA for Bitcoin"""
    sma = calculate_sma("BTC/USDT", period=20)
    if sma:
        current = get_current_price("BTC/USDT")
        print(f"Current Price: ${current['price']:.2f}")
        print(f"20-Day SMA: ${sma:.2f}")
        
        if current["price"] > sma:
            print("Bitcoin is trading ABOVE the 20-day SMA (Bullish)")
        else:
            print("Bitcoin is trading BELOW the 20-day SMA (Bearish)")


# Example 8: Health Check
def check_service_health():
    """Check if the cryptocurrency server is healthy."""
    url = "http://127.0.0.1:8000/health"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data['status']}")
        print(f"Exchange: {data['exchange']}")
        print(f"Timestamp: {data['timestamp']}")
        return True
    else:
        print("Service is down!")
        return False


# ============= JAVASCRIPT/BROWSER EXAMPLES =============

"""
Example 1: Real-time Price Display (JavaScript)

<!DOCTYPE html>
<html>
<head>
    <title>Bitcoin Price Tracker</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        .price { font-size: 48px; color: green; }
        .stats { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>Bitcoin Price Tracker</h1>
    <div class="price" id="price">$--</div>
    <div class="stats" id="stats"></div>

    <script>
        function connectWebSocket() {
            const ws = new WebSocket("ws://127.0.0.1:8000/ws/updates/BTC/USDT");
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === "price_update") {
                    document.getElementById("price").textContent = "$" + data.price.toFixed(2);
                    document.getElementById("stats").innerHTML = `
                        High: $${data.high.toFixed(2)} |
                        Low: $${data.low.toFixed(2)} |
                        Volume: ${data.volume.toFixed(0)} BTC
                    `;
                }
            };
            
            ws.onerror = () => console.error("WebSocket error");
            ws.onclose = () => {
                console.log("Reconnecting...");
                setTimeout(connectWebSocket, 3000);
            };
        }
        
        connectWebSocket();
    </script>
</body>
</html>


Example 2: Fetch Price via REST API (JavaScript)

async function getCurrentPrice(symbol) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/price/${symbol}`);
        const data = await response.json();
        console.log(`${data.symbol} - $${data.price}`);
    } catch (error) {
        console.error("Error:", error);
    }
}

// Usage
getCurrentPrice("ETH/USDT");


Example 3: Polling Multiple Prices

async function pollPrices(symbols, interval = 5000) {
    setInterval(async () => {
        for (const symbol of symbols) {
            const response = await fetch(`http://127.0.0.1:8000/price/${symbol}`);
            const data = await response.json();
            console.log(`${data.symbol}: $${data.price}`);
        }
    }, interval);
}

pollPrices(["BTC/USDT", "ETH/USDT", "BNB/USDT"]);
"""

# ============= CURL EXAMPLES =============

"""
# Get current price
curl http://127.0.0.1:8000/price/BTC/USDT

# Get 7 days of historical data
curl "http://127.0.0.1:8000/history/BTC/USDT?days=7"

# Get multiple prices (sequential)
for symbol in BTC/USDT ETH/USDT BNB/USDT; do
  curl http://127.0.0.1:8000/price/$symbol
done

# Save historical data to file
curl "http://127.0.0.1:8000/history/BTC/USDT?days=30" > bitcoin_history.json

# Check service health
curl http://127.0.0.1:8000/health

# Get cache statistics
curl http://127.0.0.1:8000/cache-stats

# Stream WebSocket data (using websocat)
websocat ws://127.0.0.1:8000/ws/updates/BTC/USDT
"""


# ============= MAIN EXAMPLE RUNNER =============

if __name__ == "__main__":
    print("Cryptocurrency Data Server - Usage Examples")
    print("=" * 50)
    
    # Check if server is running
    if not check_service_health():
        print("Please start the server first: uvicorn main:app --reload")
        exit(1)
    
    print("\n1. Get Current Price")
    example_get_price()
    
    print("\n2. Get Historical Data")
    example_get_history()
    
    print("\n3. Get Multiple Prices")
    example_batch_prices()
    
    print("\n4. Price Comparison")
    example_price_comparison()
    
    print("\n5. Technical Analysis (SMA)")
    example_sma()
    
    # Uncomment for WebSocket examples (requires async)
    # print("\n6. WebSocket Stream")
    # asyncio.run(example_websocket_stream())
    
    # print("\n7. Price Alert")
    # asyncio.run(example_price_alert())
