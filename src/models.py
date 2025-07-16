"""Data models for the Ready Set Bet application."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .constants import PLAYER_TOKENS, STARTING_MONEY, PROP_BETS, EXOTIC_FINISHES
import random


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
    prop_bet_id: Optional[int] = None
    exotic_finish_id: Optional[int] = None

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

    def is_prop_bet(self) -> bool:
        """Check if this is a prop bet."""
        return self.prop_bet_id is not None

    def is_exotic_bet(self) -> bool:
        """Check if this is an exotic finish bet."""
        return self.exotic_finish_id is not None


@dataclass
class RaceResults:
    """Represents the results of a race."""
    win_horses: List[str]
    place_horses: List[str]
    show_horses: List[str]
    prop_bet_results: Dict[int, bool] = field(default_factory=dict)
    exotic_finish_results: Dict[int, bool] = field(default_factory=dict)

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
    current_race: int = 1
    max_races: int = 4
    race_active: bool = False
    players: Dict[str, Player] = field(default_factory=dict)
    current_bets: Dict[str, Bet] = field(default_factory=dict)
    locked_spots: Dict[str, str] = field(default_factory=dict)
    race_results: Optional[RaceResults] = None
    game_log: List[str] = field(default_factory=list)
    used_prop_bets: List[int] = field(default_factory=list)
    current_prop_bets: List[Dict] = field(default_factory=list)
    used_exotic_finishes: List[int] = field(default_factory=list)
    current_exotic_finishes: List[Dict] = field(default_factory=list)

    def add_player(self, name: str) -> bool:
        """Add a new player. Returns True if successful."""
        if name not in self.players:
            self.players[name] = Player(name)
            return True
        return False

    def place_bet(self, bet: Bet) -> bool:
        """Place a bet. Returns True if successful."""
        if not self.race_active:
            return False

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

    def generate_prop_bets_for_race(self):
        """Generate 5 random prop bets for the current race, excluding used ones."""
        available_props = [prop for prop in PROP_BETS if prop["id"] not in self.used_prop_bets]

        if len(available_props) < 5:
            # If we don't have enough unused prop bets, reset and use all
            self.used_prop_bets.clear()
            available_props = PROP_BETS.copy()

        selected_props = random.sample(available_props, min(5, len(available_props)))
        self.current_prop_bets = selected_props.copy()

        # Mark these prop bets as used
        for prop in selected_props:
            if prop["id"] not in self.used_prop_bets:
                self.used_prop_bets.append(prop["id"])

    def generate_exotic_finish_for_race(self):
        """Generate 1 random exotic finish for the current race, excluding used ones."""
        if self.current_race >= self.max_races:
            # No exotic finishes added on the last race
            return

        available_exotics = [exotic for exotic in EXOTIC_FINISHES if exotic["id"] not in self.used_exotic_finishes]

        if available_exotics:
            selected_exotic = random.choice(available_exotics)
            self.current_exotic_finishes.append(selected_exotic)
            self.used_exotic_finishes.append(selected_exotic["id"])

    def next_race(self):
        """Advance to the next race."""
        self.current_race += 1
        self.race_active = False
        self.current_bets.clear()
        self.locked_spots.clear()
        self.race_results = None

        # Reset all player tokens for the new race
        for player in self.players.values():
            player.reset_tokens()

        # Generate new prop bets for the next race
        self.generate_prop_bets_for_race()

        # Generate new exotic finish for the next race (except last race)
        if self.current_race < self.max_races:
            self.generate_exotic_finish_for_race()

    def start_race(self):
        """Start the current race - enable betting."""
        self.race_active = True

    def end_race(self):
        """End the current race - disable betting."""
        self.race_active = False

    def reset_game(self):
        """Reset the entire game."""
        self.current_race = 1
        self.race_active = False
        self.players.clear()
        self.current_bets.clear()
        self.locked_spots.clear()
        self.race_results = None
        self.game_log.clear()
        self.used_prop_bets.clear()
        self.current_prop_bets.clear()
        self.used_exotic_finishes.clear()
        self.current_exotic_finishes.clear()

        # Generate prop bets for race 1
        self.generate_prop_bets_for_race()

        # Generate first exotic finish for race 1
        self.generate_exotic_finish_for_race()