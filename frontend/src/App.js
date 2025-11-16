import React, { useState, useEffect } from 'react';
import './App.css';
import PriceChart from './components/PriceChart';
import HistoricalChart from './components/HistoricalChart';
import ServerStatus from './components/ServerStatus';
import PriceCard from './components/PriceCard';

function App() {
  const [symbols] = useState(['BTC/USDT', 'ETH/USDT', 'BNBS/USDT']);
  const [selectedSymbol, setSelectedSymbol] = useState('BTC/USDT');
  const [prices, setPrices] = useState({});
  const [historicalData, setHistoricalData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [wsConnected, setWsConnected] = useState(false);

  const API_BASE = 'http://127.0.0.1:8000';

  // Fetch current prices
  useEffect(() => {
    const fetchPrices = async () => {
      try {
        setLoading(true);
        const newPrices = {};
        for (const symbol of symbols) {
          try {
            const response = await fetch(`${API_BASE}/price/${symbol}`);
            if (response.ok) {
              const data = await response.json();
              newPrices[symbol] = data;
            }
          } catch (err) {
            console.error(`Error fetching ${symbol}:`, err);
          }
        }
        setPrices(newPrices);
        setError(null);
      } catch (err) {
        setError('Failed to fetch prices');
      } finally {
        setLoading(false);
      }
    };

    fetchPrices();
    const interval = setInterval(fetchPrices, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, [symbols]);

  // Fetch historical data
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch(`${API_BASE}/history/${selectedSymbol}?days=30`);
        if (response.ok) {
          const data = await response.json();
          setHistoricalData(data.data || data.candles || []);
          console.log('Historical data loaded:', data.data?.length || 0, 'candles');
        } else {
          console.error('Failed to fetch history:', response.status);
        }
      } catch (err) {
        console.error('Error fetching history:', err);
      }
    };

    fetchHistory();
  }, [selectedSymbol]);

  // WebSocket for real-time updates
  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//127.0.0.1:8000/ws/updates/${selectedSymbol}`);

    ws.onopen = () => {
      console.log('WebSocket connected');
      setWsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setPrices(prev => ({
          ...prev,
          [selectedSymbol]: {
            ...prev[selectedSymbol],
            price: data.close,
            timestamp: new Date().toISOString()
          }
        }));
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    };

    ws.onerror = (err) => {
      console.error('WebSocket error:', err);
      setWsConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setWsConnected(false);
    };

    return () => ws.close();
  }, [selectedSymbol]);

  return (
    <div className="App">
      <header className="App-header">
        <div className="header-content">
          <h1>💰 Cryptocurrency Dashboard</h1>
          <p className="subtitle">Real-time market data powered by MCP Server</p>
        </div>
        <ServerStatus />
      </header>

      <main className="App-main">
        {error && <div className="error-banner">{error}</div>}

        {/* Price Cards Section */}
        <section className="price-cards-section">
          <h2>Current Prices</h2>
          <div className="price-cards">
            {symbols.map(symbol => (
              <PriceCard
                key={symbol}
                symbol={symbol}
                price={prices[symbol]}
                isSelected={selectedSymbol === symbol}
                onSelect={() => setSelectedSymbol(symbol)}
                loading={loading}
              />
            ))}
          </div>
        </section>

        {/* Charts Section */}
        <section className="charts-section">
          <div className="chart-container">
            <div className="chart">
              <h3>Real-time Price ({selectedSymbol})</h3>
              {wsConnected && <span className="ws-indicator">● Live</span>}
              <PriceChart symbol={selectedSymbol} price={prices[selectedSymbol]} />
            </div>

            <div className="chart">
              <h3>30-Day Historical Data ({selectedSymbol})</h3>
              <HistoricalChart data={historicalData} />
            </div>
          </div>
        </section>

        {/* Details Section */}
        <section className="details-section">
          <div className="detail-card">
            <h3>Selected Symbol Details</h3>
            {prices[selectedSymbol] ? (
              <div className="detail-grid">
                <div className="detail-item">
                  <span className="label">Current Price:</span>
                  <span className="value">${prices[selectedSymbol].price?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">24h High:</span>
                  <span className="value">${prices[selectedSymbol].high?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">24h Low:</span>
                  <span className="value">${prices[selectedSymbol].low?.toFixed(2) || 'N/A'}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Volume:</span>
                  <span className="value">{(prices[selectedSymbol].volume / 1e6)?.toFixed(2) || 'N/A'}M</span>
                </div>
                <div className="detail-item">
                  <span className="label">Last Update:</span>
                  <span className="value">{new Date(prices[selectedSymbol].timestamp).toLocaleTimeString()}</span>
                </div>
                <div className="detail-item">
                  <span className="label">Connection:</span>
                  <span className={`value ${wsConnected ? 'connected' : 'disconnected'}`}>
                    {wsConnected ? '🟢 Connected' : '🔴 Disconnected'}
                  </span>
                </div>
              </div>
            ) : (
              <p>Loading details...</p>
            )}
          </div>
        </section>
      </main>

      <footer className="App-footer">
        <p>Cryptocurrency Data Server v2.0 | MCP-Ready | Real-time Market Data</p>
        <p>📚 <a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">API Documentation</a></p>
      </footer>
    </div>
  );
}

export default App;
