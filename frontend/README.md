# Crypto Dashboard - React Frontend

Professional React dashboard for the Cryptocurrency Data Server with real-time market data, WebSocket streaming, and historical price charts.

## Features ✨

- **Real-time Price Updates** - WebSocket streaming for live cryptocurrency prices
- **Historical Charts** - 30-day OHLCV data visualization
- **Price Monitoring** - Track multiple cryptocurrencies simultaneously
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Theme** - Modern UI with gradient backgrounds and smooth animations
- **Server Status** - Real-time server connectivity indicator
- **Performance Metrics** - API usage and health statistics

## Tech Stack 🛠️

- **React 18.2** - UI framework
- **Recharts** - Data visualization and charting
- **Axios** - HTTP client (optional)
- **CSS3** - Styling with animations

## Installation 📦

### Prerequisites
- Node.js 14+ installed
- npm or yarn package manager

### Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## Usage 🚀

### Starting the Dashboard

```bash
# Development mode (with hot reload)
npm start

# Production build
npm build

# Run tests
npm test
```

## Configuration ⚙️

The frontend expects the API server running at `http://127.0.0.1:8000`

To change the API base URL, edit `frontend/src/App.js`:

```javascript
const API_BASE = 'http://127.0.0.1:8000'; // Change this line
```

## Project Structure 📁

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── PriceCard.js         # Individual price display
│   │   ├── PriceCard.css
│   │   ├── PriceChart.js        # Real-time price chart
│   │   ├── HistoricalChart.js   # 30-day historical data
│   │   ├── ServerStatus.js      # Server status indicator
│   │   └── ServerStatus.css
│   ├── App.js                   # Main application
│   ├── App.css                  # Global styles
│   ├── index.js                 # React entry point
│   └── index.css                # Global styles
├── package.json
└── README.md
```

## Components 🧩

### PriceCard
Displays current price for a cryptocurrency with 24h high/low

```jsx
<PriceCard
  symbol="BTC/USDT"
  price={price}
  isSelected={true}
  onSelect={handleSelect}
  loading={false}
/>
```

### PriceChart
Shows real-time price updates using WebSocket with Recharts

### HistoricalChart
Displays 30-day OHLCV data with volume bars and trend lines

### ServerStatus
Monitors API server health and connection status

## API Integration 🔌

### Endpoints Used

- `GET /` - Server status
- `GET /price/{symbol}` - Current price data
- `GET /history/{symbol}?days=30` - Historical candles
- `GET /health` - Health check
- `GET /metrics` - Performance metrics
- `WebSocket /ws/updates/{symbol}` - Real-time price streaming

## Styling 🎨

The dashboard uses a modern dark theme with:
- Gradient backgrounds
- Green accent color (#4CAF50)
- Smooth animations
- Responsive grid layouts
- Glassmorphism effects

Customize colors in:
- `src/App.css` - Global styles
- `src/components/*.css` - Component-specific styles

## Performance Optimization ⚡

- React.memo for component memoization
- Efficient WebSocket reconnection
- Local state management for charts
- Responsive image loading
- CSS animations instead of JavaScript

## Browser Support 🌐

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Deployment 🚀

### Build for Production

```bash
npm run build
```

Creates optimized build in `build/` directory

### Deploy to Static Host

```bash
# Vercel
npm i -g vercel
vercel

# Netlify
npm i -g netlify-cli
netlify deploy

# GitHub Pages
npm run build
npm install gh-pages --save-dev
```

### Docker Deployment

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=build /app/build ./build
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
```

## Environment Variables 🔐

Create `.env` file:

```
REACT_APP_API_BASE=http://127.0.0.1:8000
REACT_APP_API_TIMEOUT=10000
```

## Troubleshooting 🔧

### WebSocket Connection Failed
- Ensure FastAPI server is running
- Check CORS settings in API
- Verify API URL in App.js

### Charts Not Displaying
- Check browser console for errors
- Verify API endpoints are accessible
- Ensure Recharts is properly installed

### CORS Issues
- The API server has CORS enabled
- If deploying separately, configure CORS headers in API

## Development Tips 💡

### Enable Hot Reload
```bash
npm start
```

### Debug Components
Use React Developer Tools browser extension

### Check Network Requests
Open browser DevTools → Network tab

### Monitor WebSocket
DevTools → Network → WS

## Performance Tips 🚀

1. **Lazy Load Charts** - Load charts only when visible
2. **Memoize Components** - Use React.memo for expensive renders
3. **Virtual Scrolling** - For large price lists
4. **Optimize Bundle** - Use code splitting

## Contributing 🤝

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## License 📄

MIT License - See LICENSE file for details

## Support 📞

For issues or questions:
1. Check the [Main README](../README.md)
2. Review [API Documentation](http://127.0.0.1:8000/docs)
3. Open an issue on GitHub

---

**Built with ❤️ for the MCP Crypto Server**

**Last Updated**: November 2025  
**Status**: Production Ready ✅
