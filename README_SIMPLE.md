# 🎰 Ready Set Bet - Multiplayer Setup (SUPER SIMPLE!)

## 🚀 One Script, Done!

### For You (The Host):

**1. Run ONE script:**
```
Double-click: BUILD_AND_SHARE.bat
```

Wait 10-15 minutes (go get coffee ☕)

**2. Find your files in `dist_final` folder:**
- `ReadySetBet-Launcher.exe` - **For YOU**
- `ReadySetBet-Game.exe` - **For YOUR FRIENDS**

**3. Send `ReadySetBet-Game.exe` to your friends** (via Discord, email, USB, etc.)

**That's it!** 🎉

---

## 🎮 How to Play

### You (Host):

1. **Double-click `ReadySetBet-Launcher.exe`**

2. **Click "Start Server"**
   - It will show something like: `ws://73.45.123.89:8000`
   - **IMPORTANT**: Copy this address!

3. **Click "Play Multiplayer"**
   - Server: `ws://localhost:8000` (or your IP)
   - Create a session
   - You'll get a code like: `ABC123XY`

4. **Tell your friends:**
   - "Connect to: `ws://73.45.123.89:8000`"
   - "Session code: `ABC123XY`"

### Your Friends:

1. **Double-click `ReadySetBet-Game.exe`** (the file you sent them)

2. **Enter:**
   - Name: (their name)
   - Server: `ws://73.45.123.89:8000` (the address you gave them)
   - Session: `ABC123XY` (the code you gave them)

3. **Click "Join Game"**

4. **Play!** 🎰🏇

---

## 🌐 Internet Setup (Important!)

For friends to connect over the internet, you need **ONE** of these:

### Option A: Tailscale (EASIEST - Recommended!)

1. Install Tailscale (free): https://tailscale.com/download
2. Friends install it too
3. Invite them to your network
4. Use your Tailscale IP (e.g., `ws://100.64.1.5:8000`)
5. **No port forwarding needed!**

### Option B: Port Forwarding (Traditional)

1. Log into your router (usually `192.168.1.1`)
2. Find "Port Forwarding" section
3. Forward port `8000` to your computer's IP
4. Use your public IP (from whatismyipaddress.com)

See [LAUNCHER_GUIDE.md](LAUNCHER_GUIDE.md) for detailed instructions.

---

## 📁 What Files to Share

**Only send friends ONE file:**
```
ReadySetBet-Game.exe  (about 80-100 MB)
```

**Keep for yourself:**
```
ReadySetBet-Launcher.exe
```

Friends don't need:
- ❌ Python
- ❌ Any dependencies
- ❌ The source code
- ❌ Any other files

**Just the one `.exe` file!**

---

## 💡 Quick Troubleshooting

**Build script fails?**
- Make sure you have Python installed (python.org)
- Check "Add Python to PATH" when installing Python
- Try: `python --version` (should be 3.7+)
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Friends can't connect?**
- Make sure server is running (don't close the console window!)
- Check you forwarded port 8000 (or use Tailscale)
- Make sure they use `ws://` not `http://`
- Test locally first with `ws://localhost:8000`

**"Windows protected your PC" message?**
- This is normal for unsigned apps
- Click "More info" → "Run anyway"
- The code is open source, it's safe!

---

## 🎯 Complete Example

**Saturday, you want to play with 3 friends:**

### Your Steps:

1. **Friday night:** Run `BUILD_AND_SHARE.bat` (10-15 min)
2. **Saturday morning:**
   - Send `ReadySetBet-Game.exe` to friends on Discord
   - They download it
3. **Saturday afternoon:**
   - Double-click `ReadySetBet-Launcher.exe`
   - Click "Start Server" → See `ws://73.45.123.89:8000`
   - Click "Play Multiplayer" → Create session → Get code `XY8K2L4M`
   - Tell friends in Discord: "Connect to `ws://73.45.123.89:8000`, join `XY8K2L4M`"
4. **Friends:**
   - Double-click `ReadySetBet-Game.exe`
   - Enter your address and code
   - Everyone plays! 🎉

---

## ⚡ TL;DR (Too Long, Didn't Read)

```
1. Run:        BUILD_AND_SHARE.bat
2. Send to friends:  dist_final\ReadySetBet-Game.exe
3. You run:    dist_final\ReadySetBet-Launcher.exe
4. Start server, share IP and session code
5. Friends double-click the .exe and join
6. Play! 🎰
```

**That's literally it!**

---

## 📚 More Help

- **[LAUNCHER_GUIDE.md](LAUNCHER_GUIDE.md)** - Detailed launcher guide
- **[HOST_FROM_HOME.md](HOST_FROM_HOME.md)** - Network/port forwarding help
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Fix problems
- **[SIMPLE_SETUP.md](SIMPLE_SETUP.md)** - Alternative .exe building

---

**Questions? Check the troubleshooting guide or documentation!**

**Ready? Just run `BUILD_AND_SHARE.bat` and you're done! 🚀**
