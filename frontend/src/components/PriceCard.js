import React from 'react';
import './PriceCard.css';

function PriceCard({ symbol, price, isSelected, onSelect, loading }) {
  return (
    <div 
      className={`price-card ${isSelected ? 'selected' : ''} ${loading ? 'loading' : ''}`}
      onClick={onSelect}
    >
      <div className="card-header">
        <h3>{symbol}</h3>
        {isSelected && <span className="badge">Selected</span>}
      </div>

      {loading ? (
        <div className="loading-skeleton">
          <div className="skeleton-line"></div>
        </div>
      ) : price ? (
        <div className="card-content">
          <div className="price-display">
            <span className="price">${price.price?.toFixed(2) || 'N/A'}</span>
          </div>

          <div className="price-stats">
            <div className="stat">
              <span className="label">24h High</span>
              <span className="value">${price.high?.toFixed(2) || 'N/A'}</span>
            </div>
            <div className="stat">
              <span className="label">24h Low</span>
              <span className="value">${price.low?.toFixed(2) || 'N/A'}</span>
            </div>
          </div>

          <div className="timestamp">
            Last updated: {new Date(price.timestamp).toLocaleTimeString()}
          </div>
        </div>
      ) : (
        <div className="no-data">No data available</div>
      )}
    </div>
  );
}

export default PriceCard;
