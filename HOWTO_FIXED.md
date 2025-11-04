# 🎮 Ready Set Bet - How To Play (FIXED & SIMPLE!)

## 🚀 The Fixed Workflow

All the confusion is now fixed! Here's the crystal-clear workflow:

---

## Step 1: Build Everything (ONE TIME)

```
Double-click: BUILD_AND_SHARE.bat
Wait 10-15 minutes
```

You'll get 2 files in `dist_final/`:
- `ReadySetBet-Server.exe` - For you (host)
- `ReadySetBet-Game.exe` - For everyone (host + friends)

**Send `ReadySetBet-Game.exe` to your friends!**

---

## Step 2: YOU (The Host) - Start Playing

### 2.1 Start the Server
```
Double-click: ReadySetBet-Server.exe
```

You'll see a window with a big "Start Server" button.

**Click it!**

The window will show:
```
✅ Server running!

Share with friends: ws://73.45.123.89:8000

Now run 'ReadySetBet-Game.exe' to play!
```

**Copy that address!** (e.g., `ws://73.45.123.89:8000`)

**Keep this window open!** Don't close it while playing.

### 2.2 Join Your Own Server
```
Double-click: ReadySetBet-Game.exe
```

You'll see a lobby with TWO sections:

**Section 1: "HOST A GAME"** (green box)
- This is for you!
- Enter your name at the top
- Click "Create New Session"
- You'll get a code like: `ABC123XY`
- **Copy this code!**

### 2.3 Tell Your Friends

Send them:
1. The IP address: `ws://73.45.123.89:8000`
2. The session code: `ABC123XY`
3. The file: `ReadySetBet-Game.exe` (if they don't have it)

---

## Step 3: FRIENDS - Join the Game

### 3.1 Get the Files
Your friend sends you `ReadySetBet-Game.exe`

### 3.2 Run and Join
```
Double-click: ReadySetBet-Game.exe
```

You'll see a lobby with TWO sections:

**Section 2: "JOIN A FRIEND'S GAME"** (blue box)
- This is for friends!
- Enter your name at the top
- In "Server Address": Enter the address your friend gave you (e.g., `ws://73.45.123.89:8000`)
- In "Session Code": Enter the code your friend gave you (e.g., `ABC123XY`)
- Click "Join Session"

**You're in!** 🎉

---

## Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│  Lobby Screen (ReadySetBet-Game.exe)                   │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Your Name: [________________]  ← Everyone fills this   │
│                                                         │
│  ═══════════════════════════════════════════════════   │
│                                                         │
│  ┌────────────────────────────────────────┐           │
│  │  🖥️  HOST A GAME (green)               │           │
│  │                                        │           │
│  │  Use if server runs on THIS computer  │           │
│  │                                        │           │
│  │  [🎲 Create New Session]              │  ← Host   │
│  │                                        │     clicks│
│  └────────────────────────────────────────┘           │
│                                                         │
│  ═══════════════════════════════════════════════════   │
│                                                         │
│  ┌────────────────────────────────────────┐           │
│  │  🎮  JOIN A FRIEND'S GAME (blue)       │           │
│  │                                        │           │
│  │  Server Address:                       │           │
│  │  [ws://73.45.123.89:8000]             │           │
│  │                                        │           │
│  │  Session Code:                         │           │
│  │  [ABC123XY]                           │  ← Friends │
│  │                                        │     fill  │
│  │  [🚀 Join Session]                    │     this  │
│  │                                        │           │
│  └────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Summary

**Host workflow:**
1. `ReadySetBet-Server.exe` → Click "Start Server" → Get IP
2. `ReadySetBet-Game.exe` → GREEN section → "Create New Session" → Get code
3. Share IP + code with friends

**Friend workflow:**
1. `ReadySetBet-Game.exe` → BLUE section → Enter IP + code → "Join Session"
2. Play!

---

## ❓ FAQ

**Q: Which .exe file should I send to friends?**
A: `ReadySetBet-Game.exe` ONLY. They don't need the Server.exe.

**Q: Do I need to run both Server.exe and Game.exe?**
A: YES! Server.exe starts the server, Game.exe is the actual game.

**Q: Why are there two buttons in the lobby?**
A: GREEN = Host (you), BLUE = Join (friends). It's the same .exe but with 2 options.

**Q: What's the difference between "Create" and "Join"?**
- **Create** = Start a new game on localhost (assumes server is running on your PC)
- **Join** = Connect to someone else's server (need their IP address)

**Q: Friends can't connect?**
A: Make sure:
- ✅ Server.exe is running (window is open)
- ✅ Port 8000 is forwarded (or use Tailscale VPN)
- ✅ Firewall allows port 8000
- ✅ You gave them your PUBLIC IP (not 192.168.x.x)

---

## 🌐 Network Setup

**Option A: Tailscale (Easiest!)**
1. Install Tailscale (free): https://tailscale.com
2. Friends install it and join your network
3. Use your Tailscale IP (e.g., `ws://100.64.1.5:8000`)
4. No port forwarding needed!

**Option B: Port Forwarding**
1. Router → Port Forwarding → Forward port 8000 to your PC
2. Find your public IP: https://whatismyipaddress.com
3. Share: `ws://YOUR_PUBLIC_IP:8000`

---

## ✅ Checklist

Before playing:
- [ ] Ran `BUILD_AND_SHARE.bat` (done once)
- [ ] Sent `ReadySetBet-Game.exe` to friends
- [ ] Started `ReadySetBet-Server.exe` (keep it open!)
- [ ] Noted the IP address shown
- [ ] Port forwarding configured (or Tailscale)
- [ ] Friends have the Game.exe file

To play:
- [ ] You run `ReadySetBet-Game.exe` → GREEN → "Create"
- [ ] You get session code
- [ ] Friends run `ReadySetBet-Game.exe` → BLUE → "Join" with your IP + code
- [ ] Everyone plays! 🎰

---

**All fixed! The UI is now clear and the workflow makes sense! 🎉**
