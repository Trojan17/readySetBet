# 🏠 Host Ready Set Bet from Your Home Computer

## Quick Setup Guide

### Step 1: Start the Server on Your Computer

**Option A: Using Docker (Recommended)**
```bash
cd readySetBet
docker-compose up
```

**Option B: Without Docker**
```bash
# Install server dependencies
pip install -r server/requirements.txt

# Start PostgreSQL (you'll need it installed)
# On Mac: brew services start postgresql
# On Ubuntu: sudo systemctl start postgresql

# Create database
createdb readysetbet

# Start server
cd readySetBet
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```

Server will start on port 8000.

---

### Step 2: Configure Your Router (Port Forwarding)

For friends to connect from the internet, you need to forward port 8000:

1. **Find your router's IP** (usually `192.168.1.1` or `192.168.0.1`)
2. **Log into your router** (check router manual for password)
3. **Find "Port Forwarding" section** (might be under Advanced/NAT/Gaming)
4. **Create a new rule:**
   - **Service Name:** Ready Set Bet
   - **External Port:** 8000
   - **Internal Port:** 8000
   - **Internal IP:** Your computer's local IP (see below)
   - **Protocol:** TCP

**Find your computer's local IP:**
```bash
# Mac/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr IPv4

# Usually something like 192.168.1.XXX
```

---

### Step 3: Find Your Public IP Address

This is what you'll share with friends:

```bash
# Run this command:
curl ifconfig.me
```

Or visit: https://whatismyipaddress.com

**Example:** `73.45.123.89`

---

### Step 4: Share Connection Info with Friends

Tell your friends to connect using:

**Server URL:** `ws://YOUR_PUBLIC_IP:8000`

**Example:** `ws://73.45.123.89:8000`

---

### Step 5: Friends Connect

Your friends should:

1. Install the game:
   ```bash
   git clone https://github.com/Trojan17/readySetBet.git
   cd readySetBet
   pip install -r requirements.txt
   ```

2. Launch the multiplayer client:
   ```bash
   python multiplayer_main.py
   ```

3. In the lobby dialog:
   - Enter their name
   - **Change Server URL to:** `ws://YOUR_PUBLIC_IP:8000`
   - Join your session code OR create their own

---

## 🔥 Firewall Configuration

### Windows Firewall

```powershell
# Allow port 8000
netsh advfirewall firewall add rule name="Ready Set Bet Server" dir=in action=allow protocol=TCP localport=8000
```

Or use Windows Defender Firewall GUI:
1. Windows Security → Firewall & network protection
2. Advanced settings → Inbound Rules → New Rule
3. Port → TCP → 8000 → Allow

### Mac Firewall

```bash
# Usually doesn't block outbound connections
# If using application firewall, allow Python/uvicorn
```

System Preferences → Security & Privacy → Firewall → Firewall Options → Add Python

### Linux (ufw)

```bash
sudo ufw allow 8000/tcp
```

---

## 🧪 Test Your Setup

### Test Locally First

1. Start server
2. Open another terminal and test:
   ```bash
   curl http://localhost:8000
   ```
   Should return: `{"status":"ok"...}`

### Test from Internet

Ask a friend to test:
```bash
curl http://YOUR_PUBLIC_IP:8000
```

If this works, your port forwarding is correct!

---

## 📱 Connection Diagram

```
Friend's Computer                 Your Router              Your Computer
     (Client)                    (Port Forward)              (Server)
        |                              |                         |
        |  ws://73.45.123.89:8000      |                         |
        |----------------------------->|                         |
        |                              |   Port 8000             |
        |                              |------------------------>|
        |                              |                         |
        |                              |   Response              |
        |                              |<------------------------|
        |<-----------------------------|                         |
        |                              |                         |
```

---

## ⚠️ Troubleshooting

### Friends Can't Connect

**Problem:** "Connection refused" or timeout

**Solutions:**
1. ✅ Check server is running: `curl http://localhost:8000`
2. ✅ Check port forwarding is configured correctly
3. ✅ Check firewall allows port 8000
4. ✅ Verify you gave them your **public** IP (not local like 192.168.x.x)
5. ✅ Make sure server is running with `--host 0.0.0.0` (not 127.0.0.1)

**Test port forwarding:**
```bash
# From friend's computer:
telnet YOUR_PUBLIC_IP 8000
# Should connect successfully
```

### Dynamic IP Changes

If your ISP gives you a dynamic IP (changes periodically):

**Option 1: Use Dynamic DNS (DDNS)**
- Sign up for free DDNS: NoIP.com, DuckDNS, etc.
- Get a hostname like `myreadysetbet.ddns.net`
- Install their client to update IP automatically
- Friends use: `ws://myreadysetbet.ddns.net:8000`

**Option 2: Check IP before each session**
```bash
# Run this each time before hosting:
curl ifconfig.me
```

### Using Mobile Hotspot

If you're using mobile hotspot or cellular internet:
- **May not work** - Carrier-grade NAT blocks incoming connections
- **Solution:** Use a cloud server instead (see MULTIPLAYER_SETUP.md)

---

## 🔒 Security Considerations

⚠️ **You're exposing port 8000 to the internet**

**Recommendations:**

1. **Only open when playing**
   ```bash
   # After game session, remove port forwarding rule
   # Or stop the server
   ```

2. **Use strong database password**
   ```bash
   # In server/.env
   DATABASE_URL=postgresql://user:STRONG_PASSWORD@localhost/readysetbet
   ```

3. **Consider VPN instead** (Hamachi, Tailscale, ZeroTier)
   - More secure
   - No port forwarding needed
   - Friends join your VPN, then use your local IP

4. **Monitor connections**
   ```bash
   # Watch server logs for suspicious activity
   ```

---

## 🌐 Alternative: Use a VPN (No Port Forwarding)

**Easier & More Secure Option:**

### Using Tailscale (Recommended)

1. **Install Tailscale** (free): https://tailscale.com
2. **Start server** on your computer normally
3. **Friends install Tailscale** and join your network
4. **Find your Tailscale IP:**
   ```bash
   tailscale ip -4
   # Example: 100.64.1.5
   ```
5. **Friends connect to:** `ws://100.64.1.5:8000`

**Benefits:**
- ✅ No port forwarding
- ✅ Encrypted connection
- ✅ No firewall config
- ✅ Works on mobile hotspot
- ✅ Free for personal use

### Using Hamachi

1. Download Hamachi
2. Create network
3. Friends join network
4. Use your Hamachi IP: `ws://25.XXX.XXX.XXX:8000`

---

## 📋 Quick Checklist

Before hosting a game:

- [ ] Server is running (`docker-compose up` or `uvicorn ...`)
- [ ] Port 8000 is forwarded in router
- [ ] Firewall allows port 8000
- [ ] You know your public IP (`curl ifconfig.me`)
- [ ] Server URL is `ws://YOUR_PUBLIC_IP:8000`
- [ ] Tested connection locally first
- [ ] Shared server URL and session code with friends

---

## 🎮 Complete Example Session

**You (Host):**
```bash
# 1. Start server
cd readySetBet
docker-compose up

# 2. Find your IP
curl ifconfig.me
# Output: 73.45.123.89

# 3. Launch your client
python multiplayer_main.py
# Server URL: ws://73.45.123.89:8000
# Create session → Get code: XY8K2L4M

# 4. Tell friends:
# "Connect to ws://73.45.123.89:8000 and join session XY8K2L4M"
```

**Friend:**
```bash
# 1. Launch client
python multiplayer_main.py

# 2. In lobby:
# Name: Bob
# Server URL: ws://73.45.123.89:8000
# Session Code: XY8K2L4M
# Click "Join Game"

# 3. Play!
```

---

## 💡 Pro Tips

1. **Keep server running** - Don't close terminal or computer goes to sleep
2. **Use a static local IP** - Configure in router DHCP settings
3. **Test with one friend first** before inviting everyone
4. **Consider a laptop** - Easier to keep running
5. **Use Discord/chat** - Communicate while playing

---

## ❓ FAQ

**Q: Do friends need to install the server?**
A: No! Only you (the host) need the server running. Friends just need the client (`multiplayer_main.py`).

**Q: Can I play too, or just host?**
A: You can play! Just launch `multiplayer_main.py` and connect to `ws://localhost:8000` or your public IP.

**Q: How many friends can connect?**
A: Up to 9 players total (including you).

**Q: Does my computer need to stay on?**
A: Yes, as long as you want the game to run.

**Q: What if my IP changes?**
A: You'll need to tell friends the new IP. Use DDNS to avoid this.

**Q: Is this secure?**
A: Basic security. For better security, use Tailscale VPN instead.

---

**Happy hosting! 🏡🎮**
