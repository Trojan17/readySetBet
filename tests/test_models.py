"""
Unit tests for the models module.
"""

import unittest
from src.models import Player, Bet, GameState, RaceResults


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")

    def test_initial_state(self):
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.money, 0)
        self.assertEqual(self.player.get_available_tokens("5"), 1)
        self.assertEqual(self.player.get_available_tokens("3"), 2)

    def test_token_usage(self):
        self.assertTrue(self.player.use_token("5"))
        self.assertEqual(self.player.get_available_tokens("5"), 0)
        self.assertFalse(self.player.use_token("5"))  # Should fail

    def test_token_return(self):
        self.player.use_token("3")
        self.player.return_token("3")
        self.assertEqual(self.player.get_available_tokens("3"), 2)

    def test_money_operations(self):
        self.player.add_money(10)
        self.assertEqual(self.player.money, 10)

        self.player.subtract_money(5)
        self.assertEqual(self.player.money, 5)

        self.player.subtract_money(10)  # Should not go below 0
        self.assertEqual(self.player.money, 0)


class TestBet(unittest.TestCase):
    def test_bet_creation(self):
        bet = Bet(
            player="TestPlayer",
            horse="7",
            bet_type="win",
            multiplier=3,
            penalty=2,
            token_value=5,
            spot_key="test_spot"
        )

        self.assertEqual(bet.potential_payout, 15)  # 5 * 3
        self.assertEqual(bet.potential_loss, 2)
        self.assertFalse(bet.is_special_bet())


class TestGameState(unittest.TestCase):
    def setUp(self):
        self.game_state = GameState()

    def test_add_player(self):
        self.assertTrue(self.game_state.add_player("Player1"))
        self.assertFalse(self.game_state.add_player("Player1"))  # Duplicate
        self.assertIn("Player1", self.game_state.players)


if __name__ == "__main__":
    unittest.main()