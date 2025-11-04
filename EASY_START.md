# 🎮 Ready Set Bet - The EASY Way!

## 🚀 No Docker, No Complex Setup!

### Want to play multiplayer with friends? Here's how:

## Step 1: Build the .exe Files

**On Windows:**
```bash
# Just double-click this file:
build_exe.bat
```

Wait 5-10 minutes while it builds.

## Step 2: Run the Game!

**Find these files in the `dist` folder:**

```
dist/
├── ReadySetBet-Launcher.exe      👈 START HERE!
├── ReadySetBet-Server.exe
├── ReadySetBet-Game.exe
└── ReadySetBet-SinglePlayer.exe
```

**Double-click `ReadySetBet-Launcher.exe`** and choose:
- 🖥️ **Start Server** - Host a game
- 🎮 **Play Multiplayer** - Join a game
- 🏠 **Play Single Player** - Play alone

## That's It! 🎉

No Docker, no WSL, no command line, no databases to configure!

---

## 🌐 Let Friends Connect

### Easy Way: Use Tailscale VPN

1. Install Tailscale (free): https://tailscale.com
2. Friends also install Tailscale
3. They join your network
4. Share your Tailscale IP (e.g., `100.64.1.5`)
5. They connect to: `ws://100.64.1.5:8000`

**No port forwarding needed!**

### Traditional Way: Port Forwarding

1. Forward port 8000 in your router
2. Find your public IP: https://whatismyipaddress.com
3. Share with friends: `ws://YOUR_IP:8000`

See [HOST_FROM_HOME.md](HOST_FROM_HOME.md) for detailed instructions.

---

## 📖 Full Documentation

- **[SIMPLE_SETUP.md](SIMPLE_SETUP.md)** - Complete .exe guide
- **[HOST_FROM_HOME.md](HOST_FROM_HOME.md)** - Network setup details
- **[MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md)** - Advanced options

---

## 🎯 Quick Example

**You (Host):**
1. Double-click `ReadySetBet-Launcher.exe`
2. Click "Start Server" → See your IP
3. Click "Play Multiplayer" → Connect to `ws://localhost:8000`
4. Create session → Get code `ABC123XY`

**Friend:**
1. Double-click `ReadySetBet-Game.exe`
2. Server: `ws://YOUR_IP:8000`
3. Session: `ABC123XY`
4. Play! 🎰

---

**No complexity, just fun! 🏇💰**
