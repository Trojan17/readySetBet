"""Game logic and business rules for Ready Set Bet."""

from typing import List, Dict, Tuple
from .models import GameState, Player, Bet, RaceResults
from .constants import VIP_CARDS, PROP_BETS
import random


class GameLogic:
    """Handles the core game logic and business rules."""

    def __init__(self, game_state: GameState):
        self.game_state = game_state

    def process_race_results(self, win_horses: List[str], place_horses: List[str], show_horses: List[str],
                           prop_results: Dict[int, bool], exotic_results: Dict[int, bool]) -> Tuple[List[str], List[str]]:
        """Process race results and calculate payouts."""
        self.game_state.race_results = RaceResults(win_horses, place_horses, show_horses, prop_results, exotic_results)

        winners = []
        losers = []

        for bet in self.game_state.current_bets.values():
            player = self.game_state.players[bet.player]

            if bet.is_prop_bet():
                # Handle prop bet
                won = self._is_winning_prop_bet(bet, prop_results)
            elif bet.is_exotic_bet():
                # Handle exotic finish bet
                won = self._is_winning_exotic_bet(bet, exotic_results)
            else:
                # Handle standard and special bets
                won = self._is_winning_bet(bet, win_horses, place_horses, show_horses)

            if won:
                payout = bet.potential_payout
                player.add_money(payout)
                bet_description = self._get_bet_description(bet)
                winners.append(f"{bet.player}: +${payout} ({bet_description})")
            else:
                if bet.penalty > 0:
                    player.subtract_money(bet.penalty)
                    bet_description = self._get_bet_description(bet)
                    losers.append(f"{bet.player}: -${bet.penalty} penalty ({bet_description})")

        # Give VIP cards to players
        self._distribute_vip_cards()

        return winners, losers

    def _get_bet_description(self, bet: Bet) -> str:
        """Get a description of the bet for display purposes."""
        if bet.is_prop_bet():
            prop_bet = next((p for p in PROP_BETS if p["id"] == bet.prop_bet_id), None)
            if prop_bet:
                return f"Prop: {prop_bet['description']} with ${bet.token_value} token"
            return f"Prop bet #{bet.prop_bet_id} with ${bet.token_value} token"
        elif bet.is_exotic_bet():
            return f"Exotic: {bet.bet_type} with ${bet.token_value} token"
        else:
            return f"{bet.bet_type} with ${bet.token_value} token"

    def _is_winning_prop_bet(self, bet: Bet, prop_results: Dict[int, bool]) -> bool:
        """Check if a prop bet is a winning bet based on manual results."""
        return prop_results.get(bet.prop_bet_id, False)

    def _is_winning_exotic_bet(self, bet: Bet, exotic_results: Dict[int, bool]) -> bool:
        """Check if an exotic finish bet is a winning bet based on manual results."""
        return exotic_results.get(bet.exotic_finish_id, False)

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
        return self.game_state.current_race > self.game_state.max_races