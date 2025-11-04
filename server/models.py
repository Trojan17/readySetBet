"""
Database models for Ready Set Bet multiplayer
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from .database import Base


class GameSession(Base):
    """Game session table - one per game instance"""
    __tablename__ = "game_sessions"

    id = Column(String(8), primary_key=True)  # Short session code (e.g., "ABC123XY")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = Column(String(20), default="waiting")  # waiting, active, completed
    current_race = Column(Integer, default=1)
    max_races = Column(Integer, default=4)
    race_active = Column(Boolean, default=False)
    max_players = Column(Integer, default=9)

    # Game state stored as JSON
    locked_spots = Column(JSON, default=dict)  # spot_key -> player_name
    used_prop_bets = Column(JSON, default=list)  # List of used prop bet IDs
    current_prop_bets = Column(JSON, default=list)  # Current race prop bets
    used_exotic_finishes = Column(JSON, default=list)  # Used exotic finish IDs
    current_exotic_finishes = Column(JSON, default=list)  # Current exotic finishes
    game_log = Column(JSON, default=list)  # Game event log

    # Relationships
    players = relationship("Player", back_populates="session", cascade="all, delete-orphan")
    bets = relationship("Bet", back_populates="session", cascade="all, delete-orphan")
    events = relationship("GameEvent", back_populates="session", cascade="all, delete-orphan")


class Player(Base):
    """Player table - one per player in a session"""
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(8), ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    player_token = Column(String(36), unique=True, nullable=False)  # UUID for reconnection
    name = Column(String(50), nullable=False)
    money = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_connected = Column(Boolean, default=True)

    # VIP cards as JSON array
    vip_cards = Column(JSON, default=list)

    # Token usage per race stored as JSON
    # Format: {"5": 0, "3": 0, "2": 0, "1": 0} (available tokens)
    tokens = Column(JSON, default={"5": 1, "3": 2, "2": 1, "1": 1})
    used_tokens = Column(JSON, default={"5": 0, "3": 0, "2": 0, "1": 0})

    # Relationships
    session = relationship("GameSession", back_populates="players")
    bets = relationship("Bet", back_populates="player", cascade="all, delete-orphan")


class Bet(Base):
    """Bet table - one per bet placed"""
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(8), ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    race_number = Column(Integer, nullable=False)

    # Bet details
    horse = Column(String(20), nullable=False)  # e.g., "7", "2/3", "Special", "Prop", "Exotic"
    bet_type = Column(String(20), nullable=False)  # "win", "place", "show", "special", "prop", "exotic"
    multiplier = Column(Integer, nullable=False)
    penalty = Column(Integer, nullable=False)
    token_value = Column(Integer, nullable=False)
    spot_key = Column(String(50), nullable=False)

    # Optional fields
    row = Column(Integer, nullable=True)
    col = Column(Integer, nullable=True)
    prop_bet_id = Column(Integer, nullable=True)
    exotic_finish_id = Column(Integer, nullable=True)

    placed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("GameSession", back_populates="bets")
    player = relationship("Player", back_populates="bets")


class GameEvent(Base):
    """Game event log - for debugging and replay"""
    __tablename__ = "game_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(8), ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)  # e.g., "bet_placed", "race_started", etc.
    event_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    player_name = Column(String(50), nullable=True)  # Which player triggered event

    # Relationships
    session = relationship("GameSession", back_populates="events")
