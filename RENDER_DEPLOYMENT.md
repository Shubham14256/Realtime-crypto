# 🚀 Deploy on Render (Crypto-Friendly Alternative)

**Why Render?** Railway blocks crypto projects. Render is crypto-friendly and free tier available.

---

## 📋 Quick Deploy Steps

### Step 1: Go to Render
1. Open https://render.com in browser
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub

### Step 2: Create New Service
1. Click **"New +"** → **"Web Service"**
2. Search for: `Shubham14256/Realtime-crypto`
3. Click **"Connect"** next to the repository

### Step 3: Configure Service
Fill in these settings:

| Field | Value |
|-------|-------|
| Name | `crypto-server` |
| Environment | `Python 3` |
| Region | `Oregon` (or your closest region) |
| Plan | `Free` |

**Build Command**:
```
pip install -r requirements.txt && cd frontend && npm install && npm run build && cd ..
```

**Start Command**:
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables**:
- `PYTHONUNBUFFERED=true`

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Render will start building (takes 3-5 minutes) ⏳
3. Watch the logs for progress

### Step 5: Access Your App
Once deployed, Render shows your URL like:
```
https://crypto-server-xxxxx.onrender.com
```

**Your live links**:
- 🌐 Dashboard: `https://crypto-server-xxxxx.onrender.com`
- 📚 API Docs: `https://crypto-server-xxxxx.onrender.com/docs`
- 💻 WebSocket: `wss://crypto-server-xxxxx.onrender.com/ws/updates/BTC/USDT`

---

## ✅ What Gets Deployed

✅ **Backend** (Python FastAPI)
- All 8 REST endpoints
- WebSocket streaming
- Caching & rate limiting

✅ **Frontend** (React)
- Built automatically during deployment
- Served as static files
- Real-time charts & monitoring

✅ **SSL/HTTPS** - Automatic

---

## 📊 Free Tier Details

**Render Free Plan Includes**:
- 1 web service
- 0.5 GB RAM
- 0.5 CPU
- 100 GB bandwidth/month
- Auto-sleep after 15 min inactivity (wake on request)

**Perfect for your project!**

---

## 🔗 Share Your Live App

Once Render deployment is complete:

```
🎉 Realtime Cryptocurrency MCP Server - LIVE ON RENDER

GitHub: https://github.com/Shubham14256/Realtime-crypto
Live App: https://crypto-server-xxxxx.onrender.com

✨ Features:
✅ Real-time cryptocurrency data (WebSocket)
✅ React dashboard with interactive charts  
✅ 8 REST API endpoints
✅ 150-300x cache performance boost
✅ 96% test coverage
✅ Rate limiting & monitoring

📚 API Docs: https://crypto-server-xxxxx.onrender.com/docs
🔄 WebSocket: Real-time price updates
```

---

## ⚠️ Important Notes

**Auto-Sleep**: Free tier sleeps after 15 min inactivity
- First request will take ~30 seconds to wake up
- Solution: Use paid plan ($7/month) to disable sleep

**Bandwidth**: 100 GB/month should be plenty
- Each price update is <1 KB
- 100 updates/second = ~8.6 GB/month max

**Storage**: Project size ~500 MB (well within limits)

---

## 🔄 Automatic Redeploys

Render automatically redeploys when you:
1. Push to `main` branch on GitHub
2. Make any changes to your repo

No need to manually deploy again!

---

## 📞 Troubleshooting

**Build fails?**
- Check build log in Render dashboard
- Verify requirements.txt is in root
- Check frontend/package.json exists

**App crashes after deploy?**
- Check logs: Dashboard → Logs
- Verify start command is correct
- Check environment variables

**WebSocket not connecting?**
- Use `wss://` in production (auto-handled)
- Check CORS is enabled (it is by default)

**App goes to sleep?**
- Free tier sleeps after 15 min inactivity
- First request takes 30 seconds to wake
- Use paid plan to prevent sleep

---

## 💰 Upgrade to Paid (Optional)

To remove auto-sleep and get better performance:
- Click service settings
- Upgrade to paid plan ($7/month)
- No more auto-sleep
- Better performance

---

## 🎉 You're Ready to Deploy!

1. Go to https://render.com
2. Sign up with GitHub
3. Create new Web Service
4. Select your Realtime-crypto repo
5. Use settings from Step 3 above
6. Click "Create Web Service"
7. Wait 3-5 minutes
8. Share the live URL! 🚀

**Total deployment time: ~5 minutes**

