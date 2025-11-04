# 🎮 Ready Set Bet - Multiplayer Edition

## Quick Start

### 🎯 Play Locally (Testing)

**Terminal 1 - Start Server:**
```bash
docker-compose up
```

**Terminal 2 - Launch Client:**
```bash
pip install -r requirements.txt
python multiplayer_main.py
```

Create a session, share the code, and have friends join!

---

### 🌐 Play Online (Production)

#### Deploy Server to Cloud

**Option A: DigitalOcean/AWS**
```bash
# On your VM:
git clone https://github.com/yourusername/readySetBet.git
cd readySetBet
docker-compose up -d
```

**Option B: Render.com** (Free tier available)
1. Connect GitHub repository
2. Create Web Service
3. Build: `pip install -r server/requirements.txt`
4. Start: `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database
6. Deploy!

#### Connect Clients

```bash
# Set your server URL
export READYSETBET_SERVER="ws://your-server-ip:8000"
python multiplayer_main.py
```

Or edit the server URL in the lobby dialog.

---

## 📁 Project Structure

```
readySetBet/
├── server/                      # Backend server
│   ├── main.py                  # FastAPI app + WebSocket
│   ├── database.py              # PostgreSQL setup
│   ├── models.py                # Database models
│   ├── session_manager.py       # Game session logic
│   ├── websocket_manager.py     # WebSocket handling
│   └── requirements.txt         # Server dependencies
├── src/                         # Client application
│   ├── multiplayer_app.py       # Multiplayer wrapper
│   ├── network_client.py        # WebSocket client
│   ├── lobby_dialog.py          # Session join/create UI
│   ├── modern_app.py            # Main app (original)
│   └── ...                      # Other game logic
├── multiplayer_main.py          # Multiplayer entry point
├── modern_main.py               # Single-player entry point
├── docker-compose.yml           # Docker setup
├── Dockerfile                   # Server container
└── MULTIPLAYER_SETUP.md         # Full documentation
```

---

## 🎲 How It Works

### Architecture

```
┌─────────────────┐
│ Desktop Client  │ ←─┐
│ (CustomTkinter) │   │
└────────┬────────┘   │
         │ WebSocket  │
         ↓            │ Real-time
┌─────────────────┐   │ Sync
│  FastAPI Server │   │
│  (Python)       │   │
└────────┬────────┘   │
         │            │
         ↓            │
┌─────────────────┐   │
│  PostgreSQL DB  │   │
└─────────────────┘   │
         ↑            │
┌────────┴────────┐   │
│ Desktop Client  │ ←─┘
│ (CustomTkinter) │
└─────────────────┘
```

### Features

✅ **Session-based multiplayer** - 8-character codes
✅ **Up to 9 players** per session
✅ **Real-time synchronization** - See bets instantly
✅ **Reconnection support** - Don't lose progress
✅ **Any player can advance** - No host privileges
✅ **Persistent state** - Survives server restarts

---

## 🔑 Key Differences from Single-Player

| Feature | Single-Player | Multiplayer |
|---------|---------------|-------------|
| **Entry point** | `modern_main.py` | `multiplayer_main.py` |
| **Player management** | Manual "Add Player" | Auto via lobby |
| **State storage** | In-memory | PostgreSQL |
| **Betting** | Any player | Own player only |
| **Game control** | Host only | Any player |
| **Persistence** | None | Full (reconnect) |

---

## 🧪 Testing

### Test with Multiple Local Clients

```bash
# Terminal 1: Server
docker-compose up

# Terminal 2: Client 1
python multiplayer_main.py
# → Create Session → Get code ABC123XY

# Terminal 3: Client 2
python multiplayer_main.py
# → Join Session → Enter ABC123XY

# Terminal 4: Client 3
python multiplayer_main.py
# → Join Session → Enter ABC123XY
```

Place bets from different clients and watch them sync!

---

## 🛠️ Development

### Server Development

```bash
# Install dependencies
pip install -r server/requirements.txt

# Run with auto-reload
uvicorn server.main:app --reload --host 0.0.0.0 --port 8000
```

### Client Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run multiplayer client
python multiplayer_main.py

# Or run original single-player
python modern_main.py
```

---

## 📋 Environment Variables

**Server:**
- `DATABASE_URL` - PostgreSQL connection string
- `HOST` - Server bind address (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)

**Client:**
- `READYSETBET_SERVER` - WebSocket URL (default: ws://localhost:8000)

---

## 🐛 Common Issues

**"Connection refused"**
- Server not running → `docker-compose up`
- Wrong URL → Check `ws://` prefix and port

**"Session not found"**
- Invalid code → Check 8-character code
- Server restarted → Sessions cleared (use persistent volumes)

**"Cannot join session (full)"**
- Max 9 players → Start new session

**Bets not syncing**
- Check connection indicator (bottom right)
- Green = connected, Red = disconnected

---

## 📚 Full Documentation

See **[MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md)** for:
- Detailed setup instructions
- Production deployment guide
- API reference
- Security considerations
- Troubleshooting

---

## 🎯 Next Steps

1. ✅ Basic multiplayer working
2. ⏳ Add player authentication (optional)
3. ⏳ Implement spectator mode
4. ⏳ Add chat functionality
5. ⏳ Game history/statistics
6. ⏳ Leaderboards

---

## 🤝 Contributing

Pull requests welcome! Please test with multiple clients before submitting.

---

**Ready? Let's play! 🏇💰**
