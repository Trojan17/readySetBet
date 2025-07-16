"""Data models for the Ready Set Bet application."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .constants import PLAYER_TOKENS, STARTING_MONEY

@dataclass
class Player:
    """Represents a player in the game."""
    name: str
    money: int = STARTING_MONEY
    vip_cards: List[Dict] = field(default_factory=list)
    tokens: Dict[str, int] = field(default_factory=lambda: PLAYER_TOKENS.copy())
    used_tokens: Dict[str, int] = field(default_factory=lambda: {"5": 0, "3": 0, "2": 0, "1": 0})

    def reset_tokens(self):
        """Reset all tokens for a new round."""
        self.used_tokens = {"5": 0, "3": 0, "2": 0, "1": 0}

    def get_available_tokens(self, token_value: str) -> int:
        """Get the number of available tokens of a specific value."""
        return self.tokens[token_value] - self.used_tokens[token_value]

    def use_token(self, token_value: str) -> bool:
        """Use a token if available. Returns True if successful."""
        if self.get_available_tokens(token_value) > 0:
            self.used_tokens[token_value] += 1
            return True
        return False

    def return_token(self, token_value: str):
        """Return a token to the available pool."""
        if self.used_tokens[token_value] > 0:
            self.used_tokens[token_value] -= 1

    def add_money(self, amount: int):
        """Add money to the player."""
        self.money += amount

    def subtract_money(self, amount: int):
        """Subtract money from the player, minimum 0."""
        self.money = max(0, self.money - amount)

@dataclass
class Bet:
    """Represents a bet placed by a player."""
    player: str
    horse: str
    bet_type: str
    multiplier: int
    penalty: int
    token_value: int
    spot_key: str
    row: Optional[int] = None
    col: Optional[int] = None

    @property
    def potential_payout(self) -> int:
        """Calculate the potential payout for this bet."""
        return self.token_value * self.multiplier

    @property
    def potential_loss(self) -> int:
        """Get the potential loss for this bet."""
        return self.penalty

    def is_special_bet(self) -> bool:
        """Check if this is a special bet."""
        return self.horse == "Special"

@dataclass
class RaceResults:
    """Represents the results of a race."""
    win_horses: List[str]
    place_horses: List[str]
    show_horses: List[str]

    def is_winner(self, horse: str, bet_type: str) -> bool:
        """Check if a horse won for a specific bet type."""
        if bet_type == "win":
            return horse in self.win_horses
        elif bet_type == "place":
            return horse in self.place_horses
        elif bet_type == "show":
            return horse in self.show_horses
        return False

@dataclass
class GameState:
    """Represents the current state of the game."""
    current_round: int = 1
    max_rounds: int = 4
    players: Dict[str, Player] = field(default_factory=dict)
    current_bets: Dict[str, Bet] = field(default_factory=dict)
    locked_spots: Dict[str, str] = field(default_factory=dict)
    race_results: Optional[RaceResults] = None
    game_log: List[str] = field(default_factory=list)

    def add_player(self, name: str) -> bool:
        """Add a new player. Returns True if successful."""
        if name not in self.players:
            self.players[name] = Player(name)
            return True
        return False

    def place_bet(self, bet: Bet) -> bool:
        """Place a bet. Returns True if successful."""
        if bet.spot_key in self.locked_spots:
            return False

        player = self.players[bet.player]
        if not player.use_token(str(bet.token_value)):
            return False

        bet_id = f"{bet.player}_{bet.horse}_{bet.bet_type}_{bet.token_value}_{len(self.current_bets)}"
        self.current_bets[bet_id] = bet
        self.locked_spots[bet.spot_key] = bet.player
        return True

    def remove_bet(self, bet_id: str) -> bool:
        """Remove a bet. Returns True if successful."""
        if bet_id not in self.current_bets:
            return False

        bet = self.current_bets[bet_id]
        player = self.players[bet.player]

        # Return token
        player.return_token(str(bet.token_value))

        # Unlock spot
        if bet.spot_key in self.locked_spots:
            del self.locked_spots[bet.spot_key]

        # Remove bet
        del self.current_bets[bet_id]
        return True

    def clear_all_bets(self):
        """Clear all bets and reset tokens."""
        for bet in self.current_bets.values():
            player = self.players[bet.player]
            player.return_token(str(bet.token_value))

        self.current_bets.clear()
        self.locked_spots.clear()

    def next_round(self):
        """Advance to the next round."""
        self.current_round += 1
        self.current_bets.clear()
        self.locked_spots.clear()
        self.race_results = None

        # Reset all player tokens
        for player in self.players.values():
            player.reset_tokens()

    def reset_game(self):
        """Reset the entire game."""
        self.current_round = 1
        self.players.clear()
        self.current_bets.clear()
        self.locked_spots.clear()
        self.race_results = None
        self.game_log.clear()
