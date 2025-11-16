import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function PriceChart({ symbol, price }) {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (price) {
      setChartData(prev => {
        const newData = [...prev, {
          time: new Date().toLocaleTimeString(),
          price: price.price,
          symbol: symbol
        }];
        // Keep only last 20 data points
        return newData.slice(-20);
      });
    }
  }, [price, symbol]);

  return (
    <div className="price-chart">
      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
            <XAxis 
              dataKey="time" 
              stroke="rgba(255, 255, 255, 0.5)"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              stroke="rgba(255, 255, 255, 0.5)"
              tick={{ fontSize: 12 }}
              domain={['dataMin - 100', 'dataMax + 100']}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'rgba(15, 12, 41, 0.95)',
                border: '1px solid rgba(76, 175, 80, 0.5)',
                borderRadius: '8px',
                color: '#ffffff'
              }}
              formatter={(value) => `$${value.toFixed(2)}`}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#4CAF50" 
              dot={{ fill: '#4CAF50', r: 4 }}
              activeDot={{ r: 6 }}
              strokeWidth={2}
              isAnimationActive={true}
            />
          </LineChart>
        </ResponsiveContainer>
      ) : (
        <div className="no-data-chart">Waiting for real-time data...</div>
      )}
    </div>
  );
}

export default PriceChart;
