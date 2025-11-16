import React from 'react';
import { ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function HistoricalChart({ data }) {
  // Transform data for chart
  const chartData = data.slice(-30).map((candle, idx) => ({
    index: idx,
    time: new Date(candle[0]).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    open: candle[1],
    high: candle[2],
    low: candle[3],
    close: candle[4],
    volume: candle[5] / 1e6 // Convert to millions for readability
  }));

  return (
    <div className="historical-chart">
      {chartData.length > 0 ? (
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
            <XAxis 
              dataKey="time" 
              stroke="rgba(255, 255, 255, 0.5)"
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              stroke="rgba(255, 255, 255, 0.5)"
              tick={{ fontSize: 12 }}
              yAxisId="left"
            />
            <YAxis 
              stroke="rgba(255, 255, 255, 0.5)"
              tick={{ fontSize: 12 }}
              yAxisId="right"
              orientation="right"
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'rgba(15, 12, 41, 0.95)',
                border: '1px solid rgba(76, 175, 80, 0.5)',
                borderRadius: '8px',
                color: '#ffffff'
              }}
              formatter={(value, name) => {
                if (name === 'volume') return [`${value.toFixed(0)}M`, name];
                return [`$${value.toFixed(2)}`, name];
              }}
            />
            <Bar 
              yAxisId="right"
              dataKey="volume" 
              fill="rgba(76, 175, 80, 0.3)" 
              name="Volume (M)"
            />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="close" 
              stroke="#4CAF50" 
              dot={{ fill: '#4CAF50', r: 3 }}
              strokeWidth={2}
              name="Close Price"
            />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="high" 
              stroke="rgba(76, 175, 80, 0.5)" 
              dot={false}
              strokeWidth={1}
              name="High"
              strokeDasharray="5 5"
            />
            <Line 
              yAxisId="left"
              type="monotone" 
              dataKey="low" 
              stroke="rgba(255, 107, 107, 0.5)" 
              dot={false}
              strokeWidth={1}
              name="Low"
              strokeDasharray="5 5"
            />
          </ComposedChart>
        </ResponsiveContainer>
      ) : (
        <div className="no-data-chart">Loading historical data...</div>
      )}
    </div>
  );
}

export default HistoricalChart;
