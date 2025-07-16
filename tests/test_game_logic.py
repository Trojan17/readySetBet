"""
Unit tests for the game logic module.
"""

import unittest
from src.models import GameState, Bet
from src.game_logic import GameLogic


class TestGameLogic(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()
        self.game_logic = GameLogic(self.game_state)

        # Add test players
        self.game_state.add_player("Player1")
        self.game_state.add_player("Player2")

    def test_winning_standard_bet(self):
        # Create a winning bet
        bet = Bet(
            player="Player1",
            horse="7",
            bet_type="win",
            multiplier=3,
            penalty=2,
            token_value=5,
            spot_key="test_spot"
        )

        self.game_state.current_bets["test_bet"] = bet

        # Process results where horse 7 wins
        winners, losers = self.game_logic.process_race_results(["7"], ["7", "6"], ["7", "6", "5"])

        self.assertEqual(len(winners), 1)
        self.assertEqual(len(losers), 0)
        self.assertEqual(self.game_state.players["Player1"].money, 15)  # 5 * 3

    def test_losing_standard_bet(self):
        # Create a losing bet
        bet = Bet(
            player="Player1",
            horse="7",
            bet_type="win",
            multiplier=3,
            penalty=2,
            token_value=5,
            spot_key="test_spot"
        )

        self.game_state.current_bets["test_bet"] = bet

        # Process results where horse 7 doesn't win
        winners, losers = self.game_logic.process_race_results(["6"], ["6", "5"], ["6", "5", "4"])

        self.assertEqual(len(winners), 0)
        self.assertEqual(len(losers), 1)
        self.assertEqual(self.game_state.players["Player1"].money, 0)  # Can't go below 0

    def test_special_bet_blue_wins(self):
        # Create a Blue Wins bet
        bet = Bet(
            player="Player1",
            horse="Special",
            bet_type="Blue Wins",
            multiplier=5,
            penalty=1,
            token_value=3,
            spot_key="special_blue"
        )

        self.game_state.current_bets["test_bet"] = bet

        # Blue horse wins
        winners, losers = self.game_logic.process_race_results(["4"], ["4", "7"], ["4", "7", "6"])

        self.assertEqual(len(winners), 1)
        self.assertEqual(self.game_state.players["Player1"].money, 15)  # 3 * 5


if __name__ == "__main__":
    unittest.main()