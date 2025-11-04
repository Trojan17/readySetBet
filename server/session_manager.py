"""
Session management for Ready Set Bet multiplayer
"""
import random
import string
import uuid
from typing import Optional, Dict, List
from datetime import datetime
from sqlalchemy.orm import Session

from .models import GameSession, Player, Bet, GameEvent


def generate_session_id() -> str:
    """Generate a random 8-character session code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_player_token() -> str:
    """Generate a UUID for player reconnection"""
    return str(uuid.uuid4())


class SessionManager:
    """Manages game sessions and state"""

    def __init__(self, db: Session):
        self.db = db

    def create_session(self) -> GameSession:
        """Create a new game session"""
        # Generate unique session ID
        while True:
            session_id = generate_session_id()
            existing = self.db.query(GameSession).filter_by(id=session_id).first()
            if not existing:
                break

        # Import game constants
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.constants import PROP_BETS, EXOTIC_FINISHES

        # Generate initial prop bets and exotic finishes
        all_prop_bet_ids = list(range(len(PROP_BETS)))
        random.shuffle(all_prop_bet_ids)
        initial_prop_bets = all_prop_bet_ids[:5]

        all_exotic_ids = list(range(len(EXOTIC_FINISHES)))
        random.shuffle(all_exotic_ids)
        first_exotic = all_exotic_ids[0]

        session = GameSession(
            id=session_id,
            status="waiting",
            current_race=1,
            max_races=4,
            race_active=False,
            max_players=9,
            locked_spots={},
            used_prop_bets=initial_prop_bets,
            current_prop_bets=[PROP_BETS[i] for i in initial_prop_bets],
            used_exotic_finishes=[first_exotic],
            current_exotic_finishes=[EXOTIC_FINISHES[first_exotic]],
            game_log=[]
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        # Log event
        self._log_event(session_id, "session_created", {})

        return session

    def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get session by ID"""
        return self.db.query(GameSession).filter_by(id=session_id).first()

    def join_session(self, session_id: str, player_name: str) -> Optional[Dict]:
        """
        Add a player to a session
        Returns dict with player info or None if failed
        """
        session = self.get_session(session_id)
        if not session:
            return None

        # Check if session is full
        active_players = self.db.query(Player).filter_by(session_id=session_id).count()
        if active_players >= session.max_players:
            return None

        # Check if name is already taken
        existing = self.db.query(Player).filter_by(
            session_id=session_id,
            name=player_name
        ).first()
        if existing:
            return None

        # Create player with initial token allocation
        player_token = generate_player_token()
        player = Player(
            session_id=session_id,
            player_token=player_token,
            name=player_name,
            money=0,
            is_connected=True,
            vip_cards=[],
            tokens={"5": 1, "3": 2, "2": 1, "1": 1},
            used_tokens={"5": 0, "3": 0, "2": 0, "1": 0}
        )

        self.db.add(player)
        self.db.commit()
        self.db.refresh(player)

        # Log event
        self._log_event(session_id, "player_joined", {"player_name": player_name})

        return {
            "player_id": player.id,
            "player_token": player_token,
            "player_name": player_name,
            "session_id": session_id
        }

    def reconnect_player(self, player_token: str) -> Optional[Dict]:
        """
        Reconnect a player using their token
        Returns player and session info or None
        """
        player = self.db.query(Player).filter_by(player_token=player_token).first()
        if not player:
            return None

        # Update connection status
        player.is_connected = True
        player.last_seen = datetime.utcnow()
        self.db.commit()

        # Log event
        self._log_event(player.session_id, "player_reconnected", {"player_name": player.name})

        return {
            "player_id": player.id,
            "player_token": player_token,
            "player_name": player.name,
            "session_id": player.session_id
        }

    def get_session_state(self, session_id: str) -> Optional[Dict]:
        """Get complete session state for synchronization"""
        session = self.get_session(session_id)
        if not session:
            return None

        # Get all players
        players = self.db.query(Player).filter_by(session_id=session_id).all()
        players_data = []
        for p in players:
            players_data.append({
                "name": p.name,
                "money": p.money,
                "vip_cards": p.vip_cards,
                "tokens": p.tokens,
                "used_tokens": p.used_tokens,
                "is_connected": p.is_connected
            })

        # Get current bets for this race
        current_bets = self.db.query(Bet).filter_by(
            session_id=session_id,
            race_number=session.current_race
        ).all()
        bets_data = []
        for b in current_bets:
            player = self.db.query(Player).filter_by(id=b.player_id).first()
            bets_data.append({
                "player": player.name if player else "Unknown",
                "horse": b.horse,
                "bet_type": b.bet_type,
                "multiplier": b.multiplier,
                "penalty": b.penalty,
                "token_value": b.token_value,
                "spot_key": b.spot_key,
                "row": b.row,
                "col": b.col,
                "prop_bet_id": b.prop_bet_id,
                "exotic_finish_id": b.exotic_finish_id
            })

        return {
            "session_id": session.id,
            "status": session.status,
            "current_race": session.current_race,
            "max_races": session.max_races,
            "race_active": session.race_active,
            "locked_spots": session.locked_spots,
            "current_prop_bets": session.current_prop_bets,
            "current_exotic_finishes": session.current_exotic_finishes,
            "game_log": session.game_log,
            "players": players_data,
            "current_bets": bets_data
        }

    def place_bet(self, session_id: str, player_name: str, bet_data: Dict) -> Optional[Dict]:
        """
        Place a bet for a player
        Returns success status and updated state
        """
        session = self.get_session(session_id)
        if not session or not session.race_active:
            return {"success": False, "error": "Race not active"}

        player = self.db.query(Player).filter_by(
            session_id=session_id,
            name=player_name
        ).first()
        if not player:
            return {"success": False, "error": "Player not found"}

        # Check if spot is locked
        spot_key = bet_data["spot_key"]
        if spot_key in session.locked_spots:
            return {"success": False, "error": "Spot already taken"}

        # Check if player has token
        token_value = str(bet_data["token_value"])
        available = player.tokens.get(token_value, 0) - player.used_tokens.get(token_value, 0)
        if available <= 0:
            return {"success": False, "error": "Token not available"}

        # Create bet
        bet = Bet(
            session_id=session_id,
            player_id=player.id,
            race_number=session.current_race,
            horse=bet_data["horse"],
            bet_type=bet_data["bet_type"],
            multiplier=bet_data["multiplier"],
            penalty=bet_data["penalty"],
            token_value=bet_data["token_value"],
            spot_key=spot_key,
            row=bet_data.get("row"),
            col=bet_data.get("col"),
            prop_bet_id=bet_data.get("prop_bet_id"),
            exotic_finish_id=bet_data.get("exotic_finish_id")
        )

        # Update player used tokens
        player.used_tokens[token_value] = player.used_tokens.get(token_value, 0) + 1

        # Lock spot
        locked_spots = session.locked_spots.copy()
        locked_spots[spot_key] = player_name
        session.locked_spots = locked_spots

        self.db.add(bet)
        self.db.commit()

        # Log event
        self._log_event(session_id, "bet_placed", {
            "player_name": player_name,
            "spot_key": spot_key,
            "token_value": bet_data["token_value"]
        })

        return {"success": True}

    def remove_bet(self, session_id: str, player_name: str, spot_key: str) -> Optional[Dict]:
        """Remove a bet (undo)"""
        session = self.get_session(session_id)
        if not session:
            return {"success": False, "error": "Session not found"}

        player = self.db.query(Player).filter_by(
            session_id=session_id,
            name=player_name
        ).first()
        if not player:
            return {"success": False, "error": "Player not found"}

        # Find and delete bet
        bet = self.db.query(Bet).filter_by(
            session_id=session_id,
            player_id=player.id,
            race_number=session.current_race,
            spot_key=spot_key
        ).first()

        if not bet:
            return {"success": False, "error": "Bet not found"}

        # Return token
        token_value = str(bet.token_value)
        player.used_tokens[token_value] = max(0, player.used_tokens.get(token_value, 0) - 1)

        # Unlock spot
        locked_spots = session.locked_spots.copy()
        if spot_key in locked_spots:
            del locked_spots[spot_key]
        session.locked_spots = locked_spots

        self.db.delete(bet)
        self.db.commit()

        # Log event
        self._log_event(session_id, "bet_removed", {
            "player_name": player_name,
            "spot_key": spot_key
        })

        return {"success": True}

    def start_race(self, session_id: str) -> bool:
        """Start a race (enable betting)"""
        session = self.get_session(session_id)
        if not session or session.race_active:
            return False

        session.race_active = True
        session.status = "active"
        self.db.commit()

        self._log_event(session_id, "race_started", {"race_number": session.current_race})
        return True

    def end_race(self, session_id: str, results: Dict) -> bool:
        """
        End a race and process results
        results = {
            "win_horses": [...],
            "place_horses": [...],
            "show_horses": [...],
            "prop_bet_results": {...},
            "exotic_finish_results": {...}
        }
        """
        session = self.get_session(session_id)
        if not session or not session.race_active:
            return False

        session.race_active = False
        self.db.commit()

        # Process results using game logic
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.game_logic import GameLogic
        from src.models import Bet as ClientBet, Player as ClientPlayer, GameState

        # Build temporary game state for processing
        players_dict = {}
        db_players = self.db.query(Player).filter_by(session_id=session_id).all()
        for db_player in db_players:
            client_player = ClientPlayer(
                name=db_player.name,
                money=db_player.money,
                vip_cards=db_player.vip_cards,
                tokens=db_player.tokens,
                used_tokens=db_player.used_tokens
            )
            players_dict[db_player.name] = client_player

        # Build bets dict
        bets_dict = {}
        db_bets = self.db.query(Bet).filter_by(
            session_id=session_id,
            race_number=session.current_race
        ).all()
        for db_bet in db_bets:
            player = self.db.query(Player).filter_by(id=db_bet.player_id).first()
            if player:
                client_bet = ClientBet(
                    player=player.name,
                    horse=db_bet.horse,
                    bet_type=db_bet.bet_type,
                    multiplier=db_bet.multiplier,
                    penalty=db_bet.penalty,
                    token_value=db_bet.token_value,
                    spot_key=db_bet.spot_key,
                    row=db_bet.row,
                    col=db_bet.col,
                    prop_bet_id=db_bet.prop_bet_id,
                    exotic_finish_id=db_bet.exotic_finish_id
                )
                bets_dict[db_bet.spot_key] = client_bet

        # Create temporary game state
        temp_state = GameState(
            current_race=session.current_race,
            max_races=session.max_races,
            race_active=session.race_active,
            players=players_dict,
            current_bets=bets_dict,
            locked_spots=session.locked_spots,
            current_prop_bets=session.current_prop_bets,
            current_exotic_finishes=session.current_exotic_finishes,
            used_prop_bets=session.used_prop_bets,
            used_exotic_finishes=session.used_exotic_finishes
        )

        # Process results
        game_logic = GameLogic(temp_state)
        winners, losers = game_logic.process_race_results(
            results["win_horses"],
            results["place_horses"],
            results["show_horses"],
            results["prop_bet_results"],
            results["exotic_finish_results"]
        )

        # Update database players with new money and VIP cards
        for db_player in db_players:
            client_player = players_dict[db_player.name]
            db_player.money = client_player.money
            db_player.vip_cards = client_player.vip_cards

        self.db.commit()

        # Log event
        self._log_event(session_id, "race_ended", {
            "race_number": session.current_race,
            "results": results,
            "winners": winners,
            "losers": losers
        })

        return True

    def next_race(self, session_id: str) -> bool:
        """Advance to next race"""
        session = self.get_session(session_id)
        if not session or session.race_active:
            return False

        # Import game constants
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.constants import PROP_BETS, EXOTIC_FINISHES
        import random

        # Clear bets from previous race
        self.db.query(Bet).filter_by(
            session_id=session_id,
            race_number=session.current_race
        ).delete()

        # Reset player tokens
        players = self.db.query(Player).filter_by(session_id=session_id).all()
        for player in players:
            player.used_tokens = {"5": 0, "3": 0, "2": 0, "1": 0}

        # Clear locked spots
        session.locked_spots = {}

        # Advance race
        session.current_race += 1

        # Check if game is complete
        if session.current_race > session.max_races:
            session.status = "completed"
            self.db.commit()
            self._log_event(session_id, "game_completed", {})
            return True

        # Generate new prop bets
        all_prop_ids = list(range(len(PROP_BETS)))
        available_props = [i for i in all_prop_ids if i not in session.used_prop_bets]
        if len(available_props) < 5:
            # Reset if we've used too many
            session.used_prop_bets = []
            available_props = all_prop_ids

        random.shuffle(available_props)
        new_prop_ids = available_props[:5]
        session.used_prop_bets = session.used_prop_bets + new_prop_ids
        session.current_prop_bets = [PROP_BETS[i] for i in new_prop_ids]

        # Generate new exotic finish
        all_exotic_ids = list(range(len(EXOTIC_FINISHES)))
        available_exotics = [i for i in all_exotic_ids if i not in session.used_exotic_finishes]
        if available_exotics:
            new_exotic_id = random.choice(available_exotics)
            session.used_exotic_finishes = session.used_exotic_finishes + [new_exotic_id]
            session.current_exotic_finishes = session.current_exotic_finishes + [EXOTIC_FINISHES[new_exotic_id]]

        self.db.commit()

        # Log event
        self._log_event(session_id, "next_race", {"race_number": session.current_race})

        return True

    def _log_event(self, session_id: str, event_type: str, event_data: Dict):
        """Log a game event"""
        event = GameEvent(
            session_id=session_id,
            event_type=event_type,
            event_data=event_data,
            player_name=event_data.get("player_name")
        )
        self.db.add(event)
        self.db.commit()
