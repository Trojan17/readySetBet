# 🎮 Ready Set Bet - Simple Setup (No Docker/WSL Needed!)

## 🚀 Super Easy Way - Just Run the .exe!

### Download Pre-built .exe (Easiest)

If you have the pre-built .exe files, just:

1. **Double-click `ReadySetBet-Launcher.exe`**
2. Choose what you want to do:
   - **Start Server** - Host a game on your computer
   - **Play Multiplayer** - Join a game
   - **Play Single Player** - Play alone

**That's it! No installation needed!** 🎉

---

## 🔨 Build Your Own .exe Files

If you want to build the .exe files yourself:

### Windows

1. **Install Python** (if you don't have it):
   - Download from: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation

2. **Download the code**:
   ```
   git clone https://github.com/Trojan17/readySetBet.git
   cd readySetBet
   ```

3. **Double-click `build_exe.bat`**
   - This will install everything needed and build the .exe files
   - Takes 5-10 minutes

4. **Find your .exe files** in the `dist` folder:
   - `ReadySetBet-Launcher.exe` - All-in-one (Recommended!)
   - `ReadySetBet-Server.exe` - Just the server
   - `ReadySetBet-Game.exe` - Just the multiplayer client
   - `ReadySetBet-SinglePlayer.exe` - Just single player

5. **Share the .exe files!**
   - You can copy these files to any Windows computer
   - No Python installation needed to run them
   - Friends can just double-click and play!

---

## 🎯 How to Use

### Host a Game (Let Friends Connect to You)

**Option 1: Using the Launcher (Easiest)**
1. Double-click `ReadySetBet-Launcher.exe`
2. Click "Start Server"
3. You'll see: "Share with friends: ws://YOUR_IP:8000"
4. Share this address with friends!
5. Click "Play Multiplayer" to join your own server
6. Create a game session and share the 8-character code

**Option 2: Using Server.exe Directly**
1. Double-click `ReadySetBet-Server.exe`
2. Server starts automatically
3. You'll see your IP address to share
4. Keep this window open while playing!

**Important: Port Forwarding**
- For internet play, you need to forward port 8000 in your router
- See [HOST_FROM_HOME.md](HOST_FROM_HOME.md) for details
- Or use the Tailscale VPN method (easier!)

### Join a Game

**Option 1: Using the Launcher**
1. Double-click `ReadySetBet-Launcher.exe`
2. Click "Play Multiplayer"
3. Enter the server address (e.g., `ws://73.45.123.89:8000`)
4. Enter the session code
5. Play!

**Option 2: Using Game.exe Directly**
1. Double-click `ReadySetBet-Game.exe`
2. Enter server address and session code
3. Play!

### Play Single Player

**Option 1: Using the Launcher**
1. Double-click `ReadySetBet-Launcher.exe`
2. Click "Play Single Player"

**Option 2: Direct**
1. Double-click `ReadySetBet-SinglePlayer.exe`

---

## 📁 What Each File Does

| File | What It Does | When to Use |
|------|-------------|-------------|
| **ReadySetBet-Launcher.exe** | All-in-one menu | **Use this!** Easiest option |
| **ReadySetBet-Server.exe** | Just runs the server | Dedicated server computer |
| **ReadySetBet-Game.exe** | Multiplayer client only | Playing on someone else's server |
| **ReadySetBet-SinglePlayer.exe** | Offline game | No internet or solo play |

---

## 🌐 Network Setup for Internet Play

### Option A: Port Forwarding (Traditional)

1. **Start the server** on your computer
2. **Forward port 8000** in your router:
   - Log into router (usually 192.168.1.1)
   - Find "Port Forwarding" or "Virtual Server"
   - Forward external port 8000 → your computer's IP, port 8000
3. **Find your public IP**: Visit https://whatismyipaddress.com
4. **Share with friends**: `ws://YOUR_PUBLIC_IP:8000`

See [HOST_FROM_HOME.md](HOST_FROM_HOME.md) for detailed instructions.

### Option B: Use Tailscale VPN (Much Easier!)

**No port forwarding needed!**

1. **Install Tailscale** (free):
   - Download: https://tailscale.com/download
   - Sign up (takes 1 minute)

2. **Start Tailscale** on your computer

3. **Friends install Tailscale** and join your network

4. **Start server** normally (no port forwarding!)

5. **Find your Tailscale IP**:
   - Open Tailscale → Click your computer → Copy IP
   - Example: `100.64.1.5`

6. **Friends connect to**: `ws://100.64.1.5:8000`

**Benefits:**
- ✅ No router configuration
- ✅ More secure (encrypted)
- ✅ Works on any network (mobile hotspot, college wifi, etc.)
- ✅ Super easy!

---

## 🐛 Troubleshooting

### "Windows protected your PC" when running .exe

This is normal for unsigned applications:
1. Click "More info"
2. Click "Run anyway"

The code is open source - you can verify it's safe!

### Friends can't connect

**Check these:**
- ✅ Server is running (keep the window open!)
- ✅ Firewall allows port 8000
- ✅ Port forwarding is set up correctly
- ✅ You shared your **public** IP (not 192.168.x.x)
- ✅ Server address starts with `ws://` (not `http://`)

**Easy test:**
Ask a friend to visit: `http://YOUR_PUBLIC_IP:8000` in their browser
- Should see: `{"status":"ok"...}`
- If not, port forwarding isn't working

**Easier solution:** Use Tailscale VPN instead!

### Server won't start

- ✅ Make sure port 8000 isn't already in use
- ✅ Check firewall isn't blocking it
- ✅ Try running as administrator (right-click → Run as administrator)

### Game crashes on startup

- ✅ Make sure all files are in the same folder
- ✅ Try rebuilding the .exe (run `build_exe.bat` again)
- ✅ Check antivirus isn't blocking it

---

## 📦 Sharing with Friends

### Send Just the .exe

Your friends need:
1. The `.exe` file(s) they want to use
2. That's it!

No Python, no dependencies, no setup!

### What to Send

**For friends who will play:**
- Send them: `ReadySetBet-Game.exe`
- They just double-click and connect to your server

**For friends who want everything:**
- Send them: `ReadySetBet-Launcher.exe`
- They can host or play

**File sizes (approximately):**
- Launcher: ~80-100 MB
- Server: ~60-80 MB
- Game: ~80-100 MB
- SinglePlayer: ~80-100 MB

---

## 🎯 Quick Start Examples

### Example 1: Playing with Friends (You Host)

**You:**
1. Double-click `ReadySetBet-Launcher.exe`
2. Click "Start Server"
3. Note your IP: `ws://73.45.123.89:8000`
4. Click "Play Multiplayer"
5. Server URL: `ws://localhost:8000` (or your IP)
6. Create session → Get code: `ABC123XY`
7. Tell friends: "Connect to ws://73.45.123.89:8000, join session ABC123XY"

**Your Friends:**
1. Double-click `ReadySetBet-Game.exe`
2. Name: Bob
3. Server: `ws://73.45.123.89:8000`
4. Session: `ABC123XY`
5. Play!

### Example 2: Using Tailscale (Easier!)

**You:**
1. Install Tailscale → Start it
2. Double-click `ReadySetBet-Launcher.exe` → Start Server
3. Your Tailscale IP: `100.64.1.5`
4. Play Multiplayer → Connect to `ws://100.64.1.5:8000`
5. Create session → Share code

**Your Friends:**
1. Install Tailscale → Join your network
2. Launch game
3. Connect to `ws://100.64.1.5:8000`
4. Enter session code
5. Play!

---

## ✅ Advantages of .exe Method

✅ **No technical knowledge needed**
✅ **No Python installation required** to run
✅ **No Docker/WSL/containers**
✅ **Just double-click and play**
✅ **Easy to share** - send file to friends
✅ **Works offline** (single player mode)
✅ **Small file size** - easy to send via Discord/email

---

## 🎮 Ready to Play!

1. Build the .exe (run `build_exe.bat`) OR use pre-built files
2. Double-click `ReadySetBet-Launcher.exe`
3. Choose your mode
4. Have fun! 🎰🏇

**Questions?** Check the [MULTIPLAYER_SETUP.md](MULTIPLAYER_SETUP.md) for more details.

---

**No Docker, No WSL, No Complexity - Just Gaming! 🎉**
