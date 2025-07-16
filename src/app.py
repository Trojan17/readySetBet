"""Main application class for Ready Set Bet."""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional

from .models import GameState, Bet
from .game_logic import GameLogic
from .ui_components import BettingBoard
from .dialogs import StandardBetDialog, SpecialBetDialog, RaceResultsDialog, AddPlayerDialog
from .constants import HORSES, MAX_ROUNDS


class ReadySetBetApp:
    """Main application class for Ready Set Bet."""

    def __init__(self, root):
        self.root = root
        self.root.title("Ready Set Bet - Betting Board")
        self.root.geometry("1200x800")

        # Initialize game state and logic
        self.game_state = GameState()
        self.game_logic = GameLogic(self.game_state)

        # UI components
        self.betting_board = None
        self.player_listbox = None
        self.results_text = None
        self.status_var = None

        self.setup_ui()

    def setup_ui(self):
        """Set up the main user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Setup UI sections
        self._setup_controls(main_frame)
        self._setup_player_info(main_frame)
        self._setup_betting_board(main_frame)
        self._setup_results(main_frame)
        self._setup_status_bar(main_frame)

    def _setup_controls(self, parent):
        """Set up the game controls."""
        control_frame = ttk.LabelFrame(parent, text="Game Controls", padding="5")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(control_frame, text=f"Round: {self.game_state.current_round}/{MAX_ROUNDS}").grid(row=0, column=0,
                                                                                                   padx=(0, 20))

        buttons = [
            ("Add Player", self.add_player),
            ("Start Race", self.start_race),
            ("End Race", self.end_race),
            ("Next Round", self.next_round),
            ("Reset Game", self.reset_game)
        ]

        for i, (text, command) in enumerate(buttons, 1):
            ttk.Button(control_frame, text=text, command=command).grid(row=0, column=i, padx=5)

    def _setup_player_info(self, parent):
        """Set up the player information section."""
        player_frame = ttk.LabelFrame(parent, text="Players", padding="5")
        player_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        listbox_frame = ttk.Frame(player_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        self.player_listbox = tk.Listbox(listbox_frame, height=8, font=("Arial", 9))
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.player_listbox.yview)
        self.player_listbox.configure(yscrollcommand=scrollbar.set)

        self.player_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _setup_betting_board(self, parent):
        """Set up the betting board."""
        betting_frame = ttk.LabelFrame(parent, text="Betting Board", padding="5")
        betting_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))

        self.betting_board = BettingBoard(betting_frame, self.on_standard_bet, self.on_special_bet)

        # Connect bet removal functionality
        self.betting_board.bets_tree.bind("<Double-1>", self.on_bet_double_click)
        self.betting_board.remove_btn.configure(command=self.remove_selected_bet)
        self.betting_board.clear_btn.configure(command=self.clear_bets)

    def _setup_results(self, parent):
        """Set up the results section."""
        results_frame = ttk.LabelFrame(parent, text="Race Results", padding="5")
        results_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.results_text = tk.Text(results_frame, height=10, width=40)
        results_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)

        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _setup_status_bar(self, parent):
        """Set up the status bar."""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to start - Add players to begin")
        status_bar = ttk.Label(parent, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    # Event handlers
    def add_player(self):
        """Add a new player to the game."""
        dialog = AddPlayerDialog(self.root, list(self.game_state.players.keys()))
        if dialog.result:
            self.game_state.add_player(dialog.result)
            self.update_player_display()
            self.status_var.set(f"Added player: {dialog.result}")

    def on_standard_bet(self, horse: str, bet_type: str, multiplier: int, penalty: int, row: int, col: int):
        """Handle standard bet placement."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        spot_key = f"{horse}_{bet_type}_{row}_{col}"
        if spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error",
                                 f"This betting spot is already taken by {self.game_state.locked_spots[spot_key]}!")
            return

        dialog = StandardBetDialog(self.root, self.game_state.players, horse, bet_type, multiplier, penalty)
        result = dialog.show()

        if result:
            bet = Bet(
                player=result["player"],
                horse=horse,
                bet_type=bet_type,
                multiplier=multiplier,
                penalty=penalty,
                token_value=result["token_value"],
                spot_key=spot_key,
                row=row,
                col=col
            )

            if self.game_state.place_bet(bet):
                self.betting_board.update_button_appearance(horse, bet_type, row, col, result["player"])
                self.update_displays()

                penalty_text = f", Lose: -${penalty}" if penalty > 0 else ", Lose: No penalty"
                self.status_var.set(
                    f"{result['player']} placed ${result['token_value']} token on Horse {horse} to {bet_type} (Win: +${result['token_value'] * multiplier}{penalty_text})")

    def on_special_bet(self, bet_name: str, multiplier: int):
        """Handle special bet placement."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        special_spot_key = f"special_{bet_name}"
        if special_spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error",
                                 f"This special bet is already taken by {self.game_state.locked_spots[special_spot_key]}!")
            return

        dialog = SpecialBetDialog(self.root, self.game_state.players, bet_name, multiplier)
        result = dialog.show()

        if result:
            penalty = 0 if bet_name == "7 Finishes 5th or Worse" else 1
            bet = Bet(
                player=result["player"],
                horse="Special",
                bet_type=bet_name,
                multiplier=multiplier,
                penalty=penalty,
                token_value=result["token_value"],
                spot_key=special_spot_key
            )

            if self.game_state.place_bet(bet):
                self.update_displays()
                self.status_var.set(
                    f"{result['player']} placed ${result['token_value']} token on special bet: {bet_name}")

    def start_race(self):
        """Start a race."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        self.status_var.set("Race in progress - Place your bets!")
        self.log_message("Race started - Betting is now open!")

    def end_race(self):
        """End the current race and process results."""
        if not self.game_state.current_bets:
            messagebox.showerror("Error", "No bets placed!")
            return

        dialog = RaceResultsDialog(self.root, HORSES)
        if dialog.result:
            winners, losers = self.game_logic.process_race_results(
                dialog.result["win"],
                dialog.result["place"],
                dialog.result["show"]
            )

            self.log_race_results(dialog.result["win"], dialog.result["place"], dialog.result["show"], winners, losers)

            # Clear bets and reset board
            self.game_state.current_bets.clear()
            self.game_state.locked_spots.clear()
            self.betting_board.reset_all_buttons()

            self.update_displays()
            self.status_var.set(f"Race {self.game_state.current_round} completed!")

    def next_round(self):
        """Advance to the next round."""
        if self.game_logic.is_game_complete():
            self.end_game()
            return

        self.game_state.next_round()
        self.betting_board.reset_all_buttons()
        self.update_displays()
        self.update_round_display()

        self.status_var.set(f"Round {self.game_state.current_round} - All tokens reset! Ready for next race!")
        self.log_message(f"Starting Round {self.game_state.current_round} - All player tokens reset")

    def reset_game(self):
        """Reset the entire game."""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            self.game_state.reset_game()
            self.betting_board.reset_all_buttons()
            self.update_displays()
            self.update_round_display()
            self.results_text.delete(1.0, tk.END)
            self.status_var.set("Game reset - Add players to begin")

    def on_bet_double_click(self, event):
        """Handle double-click on bet to remove it."""
        selection = self.betting_board.bets_tree.selection()
        if selection:
            self.remove_selected_bet()

    def remove_selected_bet(self):
        """Remove the selected bet."""
        selection = self.betting_board.bets_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a bet to remove.")
            return

        item = selection[0]
        values = self.betting_board.bets_tree.item(item, "values")

        if not values:
            return

        # Find matching bet
        player_name = values[0]
        horse_name = values[1]
        bet_type = values[2]
        token_value = values[3].replace("$", "")

        bet_to_remove = None
        bet_id_to_remove = None

        for bet_id, bet in self.game_state.current_bets.items():
            if (bet.player == player_name and
                    bet.horse == horse_name and
                    bet.bet_type == bet_type and
                    str(bet.token_value) == token_value):
                bet_to_remove = bet
                bet_id_to_remove = bet_id
                break

        if not bet_to_remove:
            messagebox.showerror("Error", "Could not find the bet to remove.")
            return

        if messagebox.askyesno("Confirm Removal",
                               f"Remove {player_name}'s ${token_value} bet on {horse_name} ({bet_type})?"):

            # Remove bet and unlock spot
            self.game_state.remove_bet(bet_id_to_remove)

            # Reset button appearance if it's a standard bet
            if not bet_to_remove.is_special_bet() and bet_to_remove.row is not None:
                self.betting_board.reset_button_appearance(
                    bet_to_remove.horse, bet_to_remove.bet_type,
                    bet_to_remove.row, bet_to_remove.col)

            self.update_displays()
            self.status_var.set(f"Removed {player_name}'s bet on {horse_name} ({bet_type})")

    def clear_bets(self):
        """Clear all bets."""
        self.game_state.clear_all_bets()
        self.betting_board.reset_all_buttons()
        self.update_displays()
        self.status_var.set("All bets cleared, tokens returned, and spots unlocked")

    def end_game(self):
        """End the game and show final results."""
        standings = self.game_logic.get_final_standings()

        result_text = "FINAL RESULTS:\n\n"
        for i, (name, money) in enumerate(standings):
            result_text += f"{i + 1}. {name}: ${money}\n"

        self.log_message(result_text)
        messagebox.showinfo("Game Over", result_text)

    # Utility methods
    def update_displays(self):
        """Update all display components."""
        self.update_player_display()
        self.betting_board.update_bets_display(self.game_state.current_bets)

    def update_player_display(self):
        """Update the player list display."""
        self.player_listbox.delete(0, tk.END)
        for player in self.game_state.players.values():
            vip_count = len(player.vip_cards)
            tokens_available = []
            for value in ["5", "3", "2", "1"]:
                available = player.get_available_tokens(value)
                total = player.tokens[value]
                tokens_available.append(f"{available}/{total}x${value}")

            tokens_str = " | ".join(tokens_available)
            self.player_listbox.insert(tk.END,
                                       f"{player.name}: ${player.money} | Tokens: {tokens_str} | VIP: {vip_count}")

    def update_round_display(self):
        """Update the round display in controls."""
        for widget in self.root.winfo_children():
            self._update_round_widget(widget)

    def _update_round_widget(self, widget):
        """Recursively update round display widgets."""
        if hasattr(widget, 'winfo_children'):
            for child in widget.winfo_children():
                if isinstance(child, ttk.Label) and "Round:" in str(child.cget("text")):
                    child.configure(text=f"Round: {self.game_state.current_round}/{MAX_ROUNDS}")
                self._update_round_widget(child)

    def log_message(self, message: str):
        """Log a message to the results display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.results_text.see(tk.END)

    def log_race_results(self, win_horses, place_horses, show_horses, winners, losers):
        """Log race results and payouts."""
        self.log_message(f"Race {self.game_state.current_round} Results:")
        self.log_message(f"WIN: Horses {', '.join(map(str, win_horses))}")
        self.log_message(f"PLACE: Horses {', '.join(map(str, place_horses))}")
        self.log_message(f"SHOW: Horses {', '.join(map(str, show_horses))}")

        if winners:
            self.log_message("Winners:")
            for winner in winners:
                self.log_message(f"  {winner}")

        if losers:
            self.log_message("Losers (penalties applied):")
            for loser in losers:
                self.log_message(f"  {loser}")

        if not winners and not losers:
            self.log_message("No bets placed this race!")