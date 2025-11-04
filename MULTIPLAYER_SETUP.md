# Ready Set Bet - Multiplayer Setup Guide

## 🎮 Overview

Ready Set Bet now supports multiplayer! Connect with friends from anywhere in the world and play together in real-time.

### Key Features

- ✅ **Up to 9 players** per game session
- ✅ **Real-time synchronization** via WebSocket
- ✅ **Reconnection support** - rejoin if you disconnect
- ✅ **Session-based** - create or join using an 8-character code
- ✅ **Any player can advance** - democratic game control
- ✅ **Internet accessible** - play with friends anywhere

---

## 🏗️ Architecture

```
Desktop Clients (CustomTkinter)
        ↕ WebSocket
FastAPI Server (Python)
        ↕
PostgreSQL Database
```

---

## 🚀 Quick Start

### Option 1: Using Docker (Recommended for Production)

1. **Install Docker and Docker Compose**

2. **Start the server:**
   ```bash
   cd readySetBet
   docker-compose up -d
   ```

3. **Install client dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch multiplayer client:**
   ```bash
   python multiplayer_main.py
   ```

### Option 2: Manual Setup (Development)

#### 1. Setup PostgreSQL Database

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

**Create database:**
```bash
sudo -u postgres psql
CREATE DATABASE readysetbet;
CREATE USER readysetbet_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE readysetbet TO readysetbet_user;
\q
```

#### 2. Setup Server

**Install server dependencies:**
```bash
cd readySetBet
pip install -r server/requirements.txt
```

**Configure environment:**
```bash
cd server
cp .env.example .env
# Edit .env with your database credentials
```

Example `.env`:
```
DATABASE_URL=postgresql://readysetbet_user:your_password@localhost:5432/readysetbet
HOST=0.0.0.0
PORT=8000
```

**Run server:**
```bash
cd ..
python -m uvicorn server.main:app --host 0.0.0.0 --port 8000
```

Server will be available at `http://localhost:8000`

#### 3. Setup Client

**Install client dependencies:**
```bash
pip install -r requirements.txt
```

**Set server URL (optional):**
```bash
export READYSETBET_SERVER="ws://your-server-ip:8000"
```

**Launch client:**
```bash
python multiplayer_main.py
```

---

## 🎯 How to Play Multiplayer

### Creating a Session

1. Launch `multiplayer_main.py`
2. Enter your display name
3. Enter server URL (default: `ws://localhost:8000`)
4. Click **"Create New Game Session"**
5. You'll receive an 8-character session code (e.g., `ABC123XY`)
6. **Share this code with friends!**

### Joining a Session

1. Launch `multiplayer_main.py`
2. Enter your display name
3. Enter the session code
4. Click **"Join Game"**

### Playing the Game

- **Any player can start/end races** - No host designation
- **Place bets** - Only for yourself (not for other players)
- **Real-time updates** - Everyone sees bets as they happen
- **Reconnection** - If you disconnect, relaunch and join with your name

---

## 🌐 Deploying to Production

### Server Deployment Options

#### Option A: Cloud VM (DigitalOcean, AWS EC2, etc.)

1. **Provision a VM** with Ubuntu 20.04+

2. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

3. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/readySetBet.git
   cd readySetBet
   ```

4. **Start services:**
   ```bash
   docker-compose up -d
   ```

5. **Configure firewall:**
   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw enable
   ```

6. **Get server IP:**
   ```bash
   curl ifconfig.me
   ```

#### Option B: Platform as a Service (Render, Heroku, etc.)

**For Render.com:**

1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r server/requirements.txt`
4. Set start command: `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
5. Add PostgreSQL database (Render provides this)
6. Set environment variable: `DATABASE_URL` (auto-populated by Render)

**For Heroku:**

1. Create `Procfile`:
   ```
   web: uvicorn server.main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy:
   ```bash
   heroku create readysetbet-multiplayer
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   ```

### SSL/HTTPS (Recommended for Production)

For secure WebSocket connections (`wss://`), use a reverse proxy:

**Nginx + Let's Encrypt:**

```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

Then clients use: `wss://yourdomain.com`

---

## 🔧 Configuration

### Server Configuration

Edit `server/.env`:

```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Server
HOST=0.0.0.0
PORT=8000

# CORS (for web clients, optional)
# CORS_ORIGINS=https://yourdomain.com
```

### Client Configuration

Set environment variable before launching:

```bash
# Linux/macOS
export READYSETBET_SERVER="ws://your-server:8000"
python multiplayer_main.py

# Windows (PowerShell)
$env:READYSETBET_SERVER="ws://your-server:8000"
python multiplayer_main.py
```

Or edit in the lobby dialog UI.

---

## 🐛 Troubleshooting

### Server Issues

**"Connection refused"**
- Check if server is running: `curl http://localhost:8000`
- Check firewall settings
- Verify PORT is not in use: `lsof -i :8000`

**Database connection errors**
- Verify PostgreSQL is running: `systemctl status postgresql`
- Check DATABASE_URL in `.env`
- Ensure database exists: `psql -l`

**WebSocket errors**
- WebSockets use same port as HTTP server
- Check for proxy/firewall blocking WebSocket upgrade
- Verify URL starts with `ws://` (or `wss://` for SSL)

### Client Issues

**"Failed to join session"**
- Verify session code is correct (8 characters)
- Check if session is full (max 9 players)
- Ensure name is not already taken

**"Not connected to server"**
- Check server URL format: `ws://host:port` (not `http://`)
- Verify server is reachable: `ping your-server-ip`
- Check network firewall rules

**Bets not syncing**
- Check WebSocket connection status (green dot in bottom right)
- Try clicking "Request State Sync" (if implemented)
- Restart client and rejoin session

---

## 📊 Database Schema

### Tables

**game_sessions**
- `id` (VARCHAR) - 8-character session code
- `status` - waiting, active, completed
- `current_race` - Current race number
- `locked_spots` (JSON) - Spot ownership map
- `current_prop_bets` (JSON) - Prop bets for race
- `current_exotic_finishes` (JSON) - Exotic finishes

**players**
- `id` (INT) - Auto-increment
- `session_id` - Foreign key to game_sessions
- `player_token` (UUID) - For reconnection
- `name` - Display name
- `money` - Current balance
- `tokens` (JSON) - Available tokens
- `used_tokens` (JSON) - Used tokens this race

**bets**
- `id` (INT) - Auto-increment
- `session_id` - Foreign key
- `player_id` - Foreign key to players
- `race_number` - Race this bet is for
- `horse`, `bet_type`, `multiplier`, `penalty`
- `token_value`, `spot_key`

**game_events**
- Event log for debugging and replay

---

## 🔐 Security Considerations

### Current Implementation

⚠️ **Note:** Current version uses display names only (no authentication)

**Recommendations for production:**

1. **Add authentication:**
   - Implement JWT tokens
   - User registration/login
   - OAuth integration

2. **Rate limiting:**
   - Prevent spam/abuse
   - Use FastAPI rate limiter

3. **Input validation:**
   - Sanitize player names
   - Validate all client inputs

4. **SSL/TLS:**
   - Use `wss://` instead of `ws://`
   - HTTPS for API endpoints

5. **Database security:**
   - Use strong passwords
   - Restrict database access
   - Regular backups

---

## 🧪 Testing Multiplayer

### Local Testing (Multiple Clients)

1. **Start server:**
   ```bash
   docker-compose up -d
   # OR
   uvicorn server.main:app --host 0.0.0.0 --port 8000
   ```

2. **Launch first client:**
   ```bash
   python multiplayer_main.py
   ```
   - Create session
   - Note session code

3. **Launch second client:**
   ```bash
   python multiplayer_main.py
   ```
   - Join session with code

4. **Test features:**
   - Place bets from both clients
   - Start/end races
   - Check synchronization

### Load Testing

Use `locust` or similar tools:

```python
# locustfile.py
from locust import task, HttpUser, between

class GameUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_session(self):
        self.client.post("/api/sessions/create")
```

Run: `locust -f locustfile.py --host http://localhost:8000`

---

## 📝 API Reference

### HTTP Endpoints

**POST /api/sessions/create**
- Creates new session
- Returns: `{session_id, success}`

**POST /api/sessions/{session_id}/join?player_name=NAME**
- Join existing session
- Returns: `{player_token, session_id, player_name}`

**POST /api/players/reconnect?player_token=TOKEN**
- Reconnect with token
- Returns: Player and session info

**GET /api/sessions/{session_id}/state**
- Get current game state
- Returns: Full state object

### WebSocket Messages

**Client → Server:**

```json
{"type": "place_bet", "data": {...}}
{"type": "remove_bet", "spot_key": "..."}
{"type": "start_race"}
{"type": "end_race", "data": {"win_horses": [...], ...}}
{"type": "next_race"}
{"type": "request_state"}
```

**Server → Client:**

```json
{"type": "state_sync", "data": {...}}
{"type": "player_connected", "player_name": "..."}
{"type": "player_disconnected", "player_name": "..."}
{"type": "race_started", "race_number": 1}
{"type": "race_ended", "race_number": 1, "results": {...}}
{"type": "game_completed"}
{"type": "error", "message": "..."}
```

---

## 🤝 Contributing

When adding multiplayer features:

1. Update both server and client
2. Test with multiple clients
3. Update this documentation
4. Consider backward compatibility

---

## 📞 Support

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions

---

## ✅ Checklist for Deployment

- [ ] PostgreSQL database running
- [ ] Server environment variables configured
- [ ] Server started and accessible
- [ ] Firewall rules configured (port 8000)
- [ ] SSL certificate installed (production)
- [ ] Client dependencies installed
- [ ] Server URL configured in client
- [ ] Tested session creation
- [ ] Tested joining sessions
- [ ] Tested gameplay with multiple clients
- [ ] Tested reconnection
- [ ] Backups configured (database)

---

**Have fun playing Ready Set Bet with friends! 🎰🏇**
