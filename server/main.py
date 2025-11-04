"""
Ready Set Bet - Multiplayer Server
FastAPI backend with WebSocket support
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Dict, Optional
import json

from .database import get_db, init_db
from .session_manager import SessionManager
from .websocket_manager import ConnectionManager

# Initialize FastAPI app
app = FastAPI(title="Ready Set Bet Multiplayer Server", version="1.0.0")

# CORS middleware for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket connection manager
manager = ConnectionManager()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("✅ Database initialized")
    print("🚀 Ready Set Bet Server is running")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Ready Set Bet Multiplayer Server",
        "version": "1.0.0"
    }


@app.post("/api/sessions/create")
async def create_session(db: Session = Depends(get_db)):
    """Create a new game session"""
    session_manager = SessionManager(db)
    session = session_manager.create_session()

    return {
        "success": True,
        "session_id": session.id,
        "message": f"Session {session.id} created"
    }


@app.post("/api/sessions/{session_id}/join")
async def join_session(session_id: str, player_name: str, db: Session = Depends(get_db)):
    """Join an existing game session"""
    session_manager = SessionManager(db)

    # Check if session exists
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Try to join
    result = session_manager.join_session(session_id, player_name)
    if not result:
        raise HTTPException(status_code=400, detail="Cannot join session (full or name taken)")

    return {
        "success": True,
        "player_token": result["player_token"],
        "session_id": result["session_id"],
        "player_name": result["player_name"]
    }


@app.post("/api/players/reconnect")
async def reconnect_player(player_token: str, db: Session = Depends(get_db)):
    """Reconnect a player using their token"""
    session_manager = SessionManager(db)
    result = session_manager.reconnect_player(player_token)

    if not result:
        raise HTTPException(status_code=404, detail="Player not found")

    return {
        "success": True,
        **result
    }


@app.get("/api/sessions/{session_id}/state")
async def get_session_state(session_id: str, db: Session = Depends(get_db)):
    """Get current state of a session"""
    session_manager = SessionManager(db)
    state = session_manager.get_session_state(session_id)

    if not state:
        raise HTTPException(status_code=404, detail="Session not found")

    return state


@app.websocket("/ws/{session_id}/{player_token}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    player_token: str,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time game communication
    """
    session_manager = SessionManager(db)

    # Verify player token and get info
    player_info = session_manager.reconnect_player(player_token)
    if not player_info or player_info["session_id"] != session_id:
        await websocket.close(code=4004, reason="Invalid credentials")
        return

    player_name = player_info["player_name"]

    # Connect player
    await manager.connect(websocket, session_id, player_name, player_token)

    try:
        # Send initial state
        state = session_manager.get_session_state(session_id)
        await manager.send_personal_message({
            "type": "state_sync",
            "data": state
        }, websocket)

        # Notify others that player connected
        await manager.broadcast_to_session(session_id, {
            "type": "player_connected",
            "player_name": player_name
        }, exclude=websocket)

        # Listen for messages
        while True:
            data = await websocket.receive_json()
            await handle_message(websocket, data, session_id, player_name, session_manager, db)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        # Notify others that player disconnected
        await manager.broadcast_to_session(session_id, {
            "type": "player_disconnected",
            "player_name": player_name
        })
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


async def handle_message(
    websocket: WebSocket,
    message: dict,
    session_id: str,
    player_name: str,
    session_manager: SessionManager,
    db: Session
):
    """Handle incoming WebSocket messages"""
    msg_type = message.get("type")

    if msg_type == "place_bet":
        # Place a bet
        bet_data = message.get("data")
        result = session_manager.place_bet(session_id, player_name, bet_data)

        if result["success"]:
            # Get updated state
            state = session_manager.get_session_state(session_id)

            # Broadcast to all players
            await manager.broadcast_to_session(session_id, {
                "type": "state_sync",
                "data": state
            })
        else:
            # Send error to requester
            await manager.send_personal_message({
                "type": "error",
                "message": result.get("error", "Failed to place bet")
            }, websocket)

    elif msg_type == "remove_bet":
        # Remove a bet
        spot_key = message.get("spot_key")
        result = session_manager.remove_bet(session_id, player_name, spot_key)

        if result["success"]:
            # Get updated state
            state = session_manager.get_session_state(session_id)

            # Broadcast to all players
            await manager.broadcast_to_session(session_id, {
                "type": "state_sync",
                "data": state
            })
        else:
            await manager.send_personal_message({
                "type": "error",
                "message": result.get("error", "Failed to remove bet")
            }, websocket)

    elif msg_type == "start_race":
        # Start the race
        success = session_manager.start_race(session_id)

        if success:
            state = session_manager.get_session_state(session_id)
            await manager.broadcast_to_session(session_id, {
                "type": "state_sync",
                "data": state
            })
            await manager.broadcast_to_session(session_id, {
                "type": "race_started",
                "race_number": state["current_race"]
            })

    elif msg_type == "end_race":
        # End the race and process results
        results = message.get("data")
        success = session_manager.end_race(session_id, results)

        if success:
            state = session_manager.get_session_state(session_id)
            await manager.broadcast_to_session(session_id, {
                "type": "state_sync",
                "data": state
            })
            await manager.broadcast_to_session(session_id, {
                "type": "race_ended",
                "race_number": state["current_race"],
                "results": results
            })

    elif msg_type == "next_race":
        # Advance to next race
        success = session_manager.next_race(session_id)

        if success:
            state = session_manager.get_session_state(session_id)
            await manager.broadcast_to_session(session_id, {
                "type": "state_sync",
                "data": state
            })

            if state["status"] == "completed":
                await manager.broadcast_to_session(session_id, {
                    "type": "game_completed"
                })

    elif msg_type == "request_state":
        # Client requesting full state sync
        state = session_manager.get_session_state(session_id)
        await manager.send_personal_message({
            "type": "state_sync",
            "data": state
        }, websocket)

    else:
        await manager.send_personal_message({
            "type": "error",
            "message": f"Unknown message type: {msg_type}"
        }, websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
