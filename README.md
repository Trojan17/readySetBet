# 🎰 Ready Set Bet - Digital Betting Board

A Python application for the Ready Set Bet board game with **multiplayer support**!

## 🎮 Features

- **Multiplayer**: Play with friends over the internet
- **Single Player**: Practice offline
- **Authentic Game Mechanics**: Exact rules from the board game
- **Token System**: 5 tokens per race (1×$5, 2×$3, 1×$2, 1×$1)
- **Special Bets**: Blue/Orange/Red Wins, Prop Bets, Exotic Finishes
- **Easy Setup**: ONE .exe file does everything

---

## 🚀 Quick Start - Multiplayer

### 1. Build the .exe (ONE TIME)
```bash
BUILD_AND_SHARE.bat
```
Wait 10-15 minutes. You'll get: `dist_final/ReadySetBet.exe`

### 2. Play!

**Host:**
- Double-click `ReadySetBet.exe`
- Click "Host a Game" (green button)
- Share the server address and session code with friends

**Join:**
- Double-click `ReadySetBet.exe`
- Click "Join a Friend's Game" (blue button)
- Enter server address and session code

**Done!** 🎉

---

## 📖 Documentation

- **[README_FINAL.md](README_FINAL.md)** - Complete multiplayer guide (START HERE!)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Fix common issues
- **[HOST_FROM_HOME.md](HOST_FROM_HOME.md)** - Network setup (port forwarding, Tailscale)
- **[MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md)** - Advanced technical details

---

## 🎯 Single Player Mode

Want to play offline?

```bash
python modern_main.py
```

---

## 🏗️ Project Structure

```
readySetBet/
├── unified_launcher.py      # Main launcher (builds to .exe)
├── BUILD_AND_SHARE.bat      # One-click build script
├── multiplayer_main.py      # Multiplayer entry point
├── modern_main.py           # Single player entry point
├── src/                     # Game logic and UI
│   ├── models.py           # Data models
│   ├── game_logic.py       # Game rules
│   ├── multiplayer_app.py  # Multiplayer wrapper
│   ├── network_client.py   # WebSocket client
│   └── ...
├── server/                  # Backend server
│   ├── main.py            # FastAPI + WebSocket
│   ├── database.py        # SQLite database
│   ├── models.py          # Database models
│   └── ...
└── assets/                 # Icons and images
```

---

## 🌐 How Multiplayer Works

1. **Host** runs the app and clicks "Host a Game"
   - Server starts automatically in background
   - Game session created
   - Gets server address + session code

2. **Friends** run the same app and click "Join a Friend's Game"
   - Enter host's server address
   - Enter session code
   - Connected!

3. **Play together** - all players see bets in real-time

---

## 🔧 Requirements

**For Running:**
- Python 3.7+
- Dependencies: `pip install -r requirements.txt`

**For Building .exe:**
- PyInstaller: `pip install pyinstaller`
- All dependencies installed

**For Multiplayer:**
- Port 8000 forwarded (or use Tailscale VPN)

---

## 🎲 Game Rules

### Betting
- Each player starts with $0
- 5 tokens per race: 1×$5, 2×$3, 1×$2, 1×$1
- One bet per spot (locked when placed)

### Payouts
- **Win**: Token Value × Multiplier
- **Loss**: Fixed penalty (not multiplied)
- Money never goes below $0

### Special Bets
- **Blue Wins** (5x): Horses 2/3, 4, 10, 11/12
- **Orange Wins** (3x): Horses 5, 9
- **Red Wins** (2x): Horses 6, 8
- **7 Finishes 5th+** (4x): Horse 7 not in top 3
- **Prop Bets** (2x-4x): 28 different propositions
- **Exotic Finishes** (4x-6x): 5 special patterns

---

## 🛠️ Development

### Tech Stack
- **Frontend**: CustomTkinter (Python GUI)
- **Backend**: FastAPI + WebSockets
- **Database**: SQLite (auto-created)
- **Architecture**: MVC pattern

### Key Components
- `unified_launcher.py` - Single entry point for everything
- `GameState` - Manages game data
- `NetworkClient` - WebSocket communication
- `SessionManager` - Server-side session handling

### Run Development Server
```bash
# Start server
python -m uvicorn server.main:app --reload

# Start client (connects to localhost)
python multiplayer_main.py
```

---

## 📦 Building from Source

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r server/requirements.txt

# Build .exe
BUILD_AND_SHARE.bat

# Or manually:
pyinstaller --name="ReadySetBet" --onefile --windowed \
  --add-data="assets;assets" \
  --add-data="src;src" \
  --add-data="server;server" \
  unified_launcher.py
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with multiple clients
5. Submit a pull request

---

## 📝 License

GPL-3.0 License

---

## 🎉 Credits

Based on the Ready Set Bet board game.

---

**Ready to play? Run `BUILD_AND_SHARE.bat` and share the .exe with friends!** 🏇💰
