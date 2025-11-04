# 🎮 Ready Set Bet Launcher Guide

## Super Simple Setup!

### Step 1: Install Dependencies (One Time Only)

**Windows:** Double-click `setup.bat`

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Launch the Game

**Just run:**
```bash
python launcher.py
```

Or double-click `launcher.py` if your system is configured for it.

---

## 🎯 What You'll See

A beautiful launcher window with 3 big buttons:

### 🖥️ Start Server
Click this to host a game on your computer.
- Opens a new console window with the server running
- Shows you what address to share with friends (e.g., `ws://73.45.123.89:8000`)
- Keep this window open while playing!

### 🎮 Play Multiplayer
Click this to join a game (yours or a friend's).
- Opens the multiplayer client
- Enter the server address and session code
- Play with friends!

### 🏠 Play Single Player
Click this to play alone on your computer.
- No internet needed
- Classic single-player mode

---

## 🌐 Playing with Friends Over the Internet

### Method 1: Using Tailscale (Recommended - Much Easier!)

1. **Install Tailscale** (free): https://tailscale.com/download
2. **Start Tailscale** on your computer
3. **Friends install Tailscale** and accept your invitation to join your network
4. **Click "Start Server"** in the launcher
5. **Get your Tailscale IP:**
   - Open Tailscale app
   - Click on your computer name
   - Copy the IP (e.g., `100.64.1.5`)
6. **Click "Play Multiplayer"**
   - Server: `ws://100.64.1.5:8000`
   - Create a session
7. **Tell friends to connect to**: `ws://100.64.1.5:8000` with your session code

**Benefits:**
- ✅ No port forwarding needed
- ✅ Works on any network (even mobile hotspot!)
- ✅ More secure (encrypted)
- ✅ Super easy setup

### Method 2: Port Forwarding (Traditional)

See [HOST_FROM_HOME.md](HOST_FROM_HOME.md) for detailed instructions.

Quick version:
1. Click "Start Server"
2. The launcher will show your public IP (e.g., `ws://73.45.123.89:8000`)
3. Forward port 8000 in your router to your computer
4. Share that address with friends

---

## 🐛 Troubleshooting

### "Missing dependencies!" error when starting server

**Solution:** Run the setup again!
```bash
# Windows:
setup.bat

# Mac/Linux:
./setup.sh
```

Or manually install:
```bash
pip install -r requirements.txt
pip install -r server/requirements.txt
```

### Launcher UI is cut off / can't see all buttons

**Solution:**
- The window is now scrollable - use mouse wheel to scroll
- Or resize the window (drag the corners)
- The launcher is now 600x700 and resizable

### Server won't start - port already in use

**Solution:**
- Another program is using port 8000
- Close any other instances of the server
- Or change the port in `server/main.py` (line with `port=8000`)

### Friends can't connect

**Check:**
- ✅ Server is running (console window is open)
- ✅ Firewall allows port 8000
- ✅ Port forwarding is configured (if not using Tailscale)
- ✅ You shared your **public** IP, not local (192.168.x.x)
- ✅ Address starts with `ws://` not `http://`

**Easy fix:** Use Tailscale instead!

### Launcher closes immediately

**Solution:** Run from command line to see errors:
```bash
python launcher.py
```

Check if Python and dependencies are installed correctly.

---

## 📝 What Each Button Does

### Start Server Button

**What it does:**
- Checks if uvicorn/fastapi are installed
- Gets your public IP address (to share with friends)
- Starts the server in a new console window
- Shows "✅ Server running! Share: ws://YOUR_IP:8000"

**Note:** Keep the console window open while playing!

### Play Multiplayer Button

**What it does:**
- Launches `multiplayer_main.py` in a new window
- Shows the lobby where you can:
  - Create a new game session
  - Join an existing session with a code
  - Enter server address and your name

### Play Single Player Button

**What it does:**
- Launches `modern_main.py` in a new window
- Classic single-player mode
- No internet or server needed

---

## 🎮 Complete Example: Playing with a Friend

### You (Host):

1. **Double-click `setup.bat`** (first time only)
2. **Double-click `launcher.py`** (or run `python launcher.py`)
3. **Click "Start Server"**
   - Wait for: "✅ Server running! Share: ws://73.45.123.89:8000"
   - Note your IP address
4. **Click "Play Multiplayer"**
   - Name: Alice
   - Server: `ws://localhost:8000` (or your IP)
   - Click "Create New Game Session"
   - You get session code: `XY8K2L4M`
5. **Tell your friend:**
   - "Connect to `ws://73.45.123.89:8000`"
   - "Join session `XY8K2L4M`"

### Your Friend:

1. **Get the game files** (from you or GitHub)
2. **Double-click `setup.bat`** (first time only)
3. **Double-click `launcher.py`** (or run `python launcher.py`)
4. **Click "Play Multiplayer"**
   - Name: Bob
   - Server: `ws://73.45.123.89:8000` (the address you gave them)
   - Session: `XY8K2L4M` (the code you gave them)
   - Click "Join Game"
5. **Play!** 🎰

### Both Players:
- Place bets during each race
- Any player can start/end races
- See each other's bets in real-time
- Have fun! 🏇

---

## 💡 Pro Tips

1. **Use Tailscale** - Makes everything much easier, no port forwarding!
2. **Keep server window open** - Don't close the console while playing
3. **Share both** - Give friends both the server address AND session code
4. **Test locally first** - Play on your own server (`ws://localhost:8000`) before inviting friends
5. **Use Discord/voice chat** - More fun to talk while playing!

---

## 🚀 Alternative: Building .exe Files

If you don't want to run Python scripts, you can build standalone .exe files:

1. Run `build_exe.bat` (takes 5-10 minutes)
2. Find .exe files in `dist/` folder
3. Double-click `ReadySetBet-Launcher.exe`
4. Share .exe files with friends (they don't need Python!)

See [SIMPLE_SETUP.md](SIMPLE_SETUP.md) for details.

---

## ✅ Advantages of the Launcher

✅ **No command line needed** - Just click buttons
✅ **All-in-one interface** - Server, multiplayer, single player
✅ **Automatic IP display** - Shows what to share with friends
✅ **Dependency checking** - Tells you if anything is missing
✅ **Easy setup** - One-time `setup.bat` and you're done
✅ **Works with Python** - No need to build .exe files
✅ **Scrollable UI** - Can see all options
✅ **Clear error messages** - Helpful troubleshooting

---

## 📞 Need Help?

- Check [HOST_FROM_HOME.md](HOST_FROM_HOME.md) for networking setup
- Check [SIMPLE_SETUP.md](SIMPLE_SETUP.md) for .exe building
- Check [MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md) for advanced options

---

**Happy Gaming! 🎰🏇**
