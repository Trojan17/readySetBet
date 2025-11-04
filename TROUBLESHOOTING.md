# 🔧 Troubleshooting Guide

## Build/Installation Errors

### Error: "Getting requirements to build wheel ... error"

**This happens when:** A package needs C++ build tools to compile.

**Quick Fix:**

1. **Use the simple setup** (avoids build issues):
   ```bash
   # Windows:
   setup_simple.bat

   # Mac/Linux:
   pip install customtkinter Pillow websockets requests
   pip install fastapi uvicorn websockets sqlalchemy python-dotenv pydantic requests
   ```

2. **If that still fails, install packages one by one:**
   ```bash
   # Try each individually to find which one fails
   pip install customtkinter
   pip install Pillow
   pip install websockets
   pip install requests
   pip install fastapi
   pip install uvicorn
   pip install sqlalchemy
   pip install python-dotenv
   pip install pydantic
   ```

3. **Common problematic packages and solutions:**

   **Pillow fails:**
   - Install pre-built version: `pip install Pillow --only-binary :all:`
   - Or: Download wheel from https://pypi.org/project/Pillow/#files

   **customtkinter fails:**
   - Update pip first: `python -m pip install --upgrade pip`
   - Then: `pip install customtkinter`

---

### Error: "Microsoft Visual C++ 14.0 or greater is required"

**On Windows, you need C++ build tools for some packages.**

**Solutions:**

**Option 1: Install pre-built wheels only** (Easiest)
```bash
pip install --only-binary :all: -r requirements.txt
pip install --only-binary :all: -r server/requirements.txt
```

**Option 2: Install Visual C++ Build Tools**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++" workload
3. Restart computer
4. Run `setup.bat` again

**Option 3: Skip problematic packages** (for now)
```bash
# Just install what you need to run
pip install customtkinter websockets requests fastapi uvicorn sqlalchemy
```

---

## Launcher Issues

### Launcher UI is cut off / can't see buttons

**Fixed in latest version!** Make sure you have the latest code:
```bash
git pull origin claude/multiplayer-game-session-011CUnwvtcghgKwXHs4tXqF7
```

**Manual fix:**
- Resize the window (drag corners)
- Use mouse wheel to scroll
- Window is now 600x700 and scrollable

---

### "No module named uvicorn" when starting server

**Solution 1: Install server dependencies**
```bash
pip install fastapi uvicorn
```

**Solution 2: Use simple setup**
```bash
setup_simple.bat
```

**Solution 3: Check if installed**
```bash
python -c "import uvicorn; print('OK')"
python -c "import fastapi; print('OK')"
```

If these fail, the packages aren't installed correctly.

---

## Server Issues

### Port 8000 already in use

**Solution:**
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill that process (replace PID with the number you see)
taskkill /PID <PID> /F
```

Or use a different port - edit `server/main.py` line with `port=8000`

---

### Server starts but friends can't connect

**Check these in order:**

1. **Test locally first:**
   ```bash
   # In browser, visit:
   http://localhost:8000
   # Should see: {"status":"ok",...}
   ```

2. **Check firewall:**
   ```bash
   # Windows - Allow port 8000
   netsh advfirewall firewall add rule name="Ready Set Bet" dir=in action=allow protocol=TCP localport=8000
   ```

3. **Test from same network:**
   ```bash
   # Get your local IP
   ipconfig
   # Look for 192.168.x.x

   # Friend on same WiFi visits:
   http://192.168.x.x:8000
   ```

4. **Check port forwarding:**
   - Log into router (usually 192.168.1.1)
   - Port Forwarding section
   - Forward external 8000 → your computer IP, port 8000
   - Protocol: TCP

5. **Get public IP:**
   ```bash
   curl ifconfig.me
   ```
   Share: `ws://YOUR_PUBLIC_IP:8000`

**Easier solution:** Use Tailscale VPN (no port forwarding needed!)
- Install: https://tailscale.com
- Friends join your network
- Share your Tailscale IP (e.g., `ws://100.64.1.5:8000`)

---

## Client Issues

### Can't connect to server

**Check:**
- ✅ Server is running (console window open)
- ✅ URL starts with `ws://` not `http://`
- ✅ Port 8000 is correct
- ✅ IP address is correct (public IP, not 192.168.x.x)

**Test connection:**
```bash
# In browser, visit:
http://YOUR_SERVER_IP:8000
# Should see: {"status":"ok",...}
```

---

### "Session not found" error

**Causes:**
- Server restarted (sessions are lost)
- Wrong session code
- Session code expired

**Solution:**
- Create a new session
- Share the new code with friends

---

### Bets not syncing

**Check:**
- ✅ Green dot in bottom right (connected)
- ✅ Same session code
- ✅ Server console shows activity

**Fix:**
- Restart client
- Reconnect to session

---

## Python Issues

### "Python is not recognized" error

**Solution:**
1. Install Python from: https://www.python.org/downloads/
2. ✅ **Check "Add Python to PATH"** during installation
3. Restart computer
4. Test: `python --version`

---

### Wrong Python version

**Check version:**
```bash
python --version
# Should be 3.7 or higher
```

**If version is too old:**
- Install newer Python from python.org
- Or use: `python3` instead of `python`

---

## SQLite Database Issues

### "Database is locked" error

**Cause:** Multiple processes accessing database

**Solution:**
```bash
# Close all game instances
# Delete database file
del readysetbet.db  # Windows
rm readysetbet.db   # Mac/Linux

# Restart server (creates new database)
```

---

### Want to reset everything

**Delete the database:**
```bash
# Stop server first
# Then delete:
del readysetbet.db  # Windows
rm readysetbet.db   # Mac/Linux

# Restart server - fresh database!
```

---

## Building .exe Issues

### PyInstaller not found

**Solution:**
```bash
pip install pyinstaller
```

---

### .exe build fails

**Common causes:**
1. **Not enough disk space** - Need ~500MB free
2. **Antivirus blocking** - Temporarily disable
3. **Missing dependencies** - Run setup first

**Solution:**
```bash
# Clean old builds
rmdir /s build dist
del *.spec

# Install dependencies
setup_simple.bat

# Install PyInstaller
pip install pyinstaller

# Try building again
build_exe.bat
```

---

### .exe runs but crashes immediately

**Debug:**
```bash
# Run from command line to see error
dist\ReadySetBet-Launcher.exe

# Or check if dependencies are included
# Add --onedir instead of --onefile for easier debugging
```

---

## Still Having Issues?

### Get detailed error information:

**Run with verbose output:**
```bash
python launcher.py 2>&1 | tee error.log
```

**Check Python environment:**
```bash
python --version
pip list
pip check
```

**Test imports:**
```bash
python -c "import customtkinter; print('customtkinter: OK')"
python -c "import fastapi; print('fastapi: OK')"
python -c "import uvicorn; print('uvicorn: OK')"
python -c "import websockets; print('websockets: OK')"
```

---

## Quick Recovery Steps

If everything is broken, start fresh:

```bash
# 1. Clean installation
pip uninstall -y customtkinter fastapi uvicorn websockets sqlalchemy requests Pillow

# 2. Update pip
python -m pip install --upgrade pip

# 3. Install fresh
pip install customtkinter Pillow websockets requests
pip install fastapi uvicorn sqlalchemy python-dotenv pydantic

# 4. Test
python launcher.py
```

---

## Alternative: Skip Dependencies

Don't need multiplayer? Just play single player:

```bash
# Only install client dependencies
pip install customtkinter Pillow

# Run single player
python modern_main.py
```

---

## Contact / Help

- GitHub Issues: https://github.com/Trojan17/readySetBet/issues
- Check documentation:
  - LAUNCHER_GUIDE.md - Launcher help
  - HOST_FROM_HOME.md - Network setup
  - SIMPLE_SETUP.md - .exe building

---

**Most Common Solutions:**
1. Use `setup_simple.bat` instead of `setup.bat`
2. Install packages one by one to find which fails
3. Use `--only-binary :all:` to avoid building from source
4. Update pip: `python -m pip install --upgrade pip`
5. Install Visual C++ Build Tools (Windows)
6. Use Tailscale instead of port forwarding
