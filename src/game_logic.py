"""Game logic and business rules for Ready Set Bet."""

from typing import List, Dict, Tuple
from .models import GameState, Player, Bet, RaceResults
from .constants import VIP_CARDS
import random


class GameLogic:
    """Handles the core game logic and business rules."""

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def process_race_results(self, win_horses: List[str], place_horses: List[str], show_horses: List[str]) -> Tuple[
        List[str], List[str]]:
        """Process race results and calculate payouts."""
        self.game_state.race_results = RaceResults(win_horses, place_horses, show_horses)

        winners = []
        losers = []

        for bet in self.game_state.current_bets.values():
            player = self.game_state.players[bet.player]
            won = self._is_winning_bet(bet, win_horses, place_horses, show_horses)

            if won:
                payout = bet.potential_payout
                player.add_money(payout)
                winners.append(f"{bet.player}: +${payout} ({bet.bet_type} with ${bet.token_value} token)")
            else:
                if bet.penalty > 0:
                    player.subtract_money(bet.penalty)
                    losers.append(
                        f"{bet.player}: -${bet.penalty} penalty ({bet.bet_type} with ${bet.token_value} token)")

        # Give VIP cards to players
        self._distribute_vip_cards()

        return winners, losers

    def _is_winning_bet(self, bet: Bet, win_horses: List[str], place_horses: List[str], show_horses: List[str]) -> bool:
        """Check if a bet is a winning bet."""
        if bet.bet_type in ["win", "place", "show"]:
            return self.game_state.race_results.is_winner(bet.horse, bet.bet_type)

        # Special bets
        if bet.bet_type == "Blue Wins":
            blue_horses = ["2/3", "4", "10", "11/12"]
            return any(horse in blue_horses for horse in win_horses)
        elif bet.bet_type == "Orange Wins":
            orange_horses = ["5", "9"]
            return any(horse in orange_horses for horse in win_horses)
        elif bet.bet_type == "Red Wins":
            red_horses = ["6", "8"]
            return any(horse in red_horses for horse in win_horses)
        elif bet.bet_type == "7 Finishes 5th or Worse":
            return "7" not in show_horses

        return False

    def _distribute_vip_cards(self):
        """Distribute VIP cards to players."""
        for player in self.game_state.players.values():
            if len(player.vip_cards) < 4:  # Max 4 VIP cards
                card = random.choice(VIP_CARDS)
                player.vip_cards.append(card)

    def get_final_standings(self) -> List[Tuple[str, int]]:
        """Get final standings sorted by money."""
        return sorted(
            [(player.name, player.money) for player in self.game_state.players.values()],
            key=lambda x: x[1],
            reverse=True
        )

    def is_game_complete(self) -> bool:
        """Check if the game is complete."""
        return self.game_state.current_round > self.game_state.max_rounds