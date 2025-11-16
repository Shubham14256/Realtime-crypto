import React, { useState, useEffect } from 'react';
import './ServerStatus.css';

function ServerStatus() {
  const [status, setStatus] = useState('checking');
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/health');
        if (response.ok) {
          setStatus('online');
        } else {
          setStatus('offline');
        }
      } catch (err) {
        setStatus('offline');
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/metrics');
        if (response.ok) {
          const data = await response.json();
          setMetrics(data);
        }
      } catch (err) {
        console.error('Error fetching metrics:', err);
      }
    };

    checkStatus();
    const interval = setInterval(checkStatus, 10000); // Check every 10 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="server-status">
      <div className={`status-badge ${status}`}>
        <span className="dot"></span>
        {status === 'online' && 'Server Online'}
        {status === 'offline' && 'Server Offline'}
        {status === 'checking' && 'Checking...'}
      </div>

      {metrics && (
        <div className="metrics-popup">
          <div className="metric-item">
            <span className="metric-label">API Requests</span>
            <span className="metric-value">{metrics.total_requests || 0}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Success Rate</span>
            <span className="metric-value">{metrics.success_rate?.toFixed(1) || '0'}%</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default ServerStatus;
