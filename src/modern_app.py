"""Modern main application class for Ready Set Bet using CustomTkinter."""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from typing import Dict, List

from .icon_utils import icon_manager
from .models import GameState, Bet
from .game_logic import GameLogic
from .modern_ui_components import ModernBettingBoard
from .modern_dialogs import (
    ModernStandardBetDialog, ModernSpecialBetDialog, ModernPropBetDialog,
    ModernExoticFinishDialog, ModernAddPlayerDialog, ModernRaceResultsDialog
)
from .constants import Theme, HORSES, MAX_RACES


class ModernReadySetBetApp:
    """Main application class."""

    def __init__(self, root):
        self.root = root
        self._setup_window()

        # Initialize game components
        self.game_state = GameState()
        self.game_logic = GameLogic(self.game_state)

        # Generate initial content
        self.game_state.generate_prop_bets_for_race()
        self.game_state.generate_exotic_finish_for_race()

        # UI components
        self.betting_board = None
        self.players_text = None
        self.results_text = None
        self.status_var = None
        self.race_label = None
        self.control_buttons = {}

        self._setup_ui()
        self._update_button_states()

    def _setup_window(self):
        """Configure the main window."""
        self.root.title("🏇 Ready Set Bet - Modern Betting Board")
        self.root.geometry("1400x900")
        self.root.configure(fg_color=Theme.SURFACE)

        # Set window icon
        icon_manager.set_window_icon(self.root)

        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def _setup_ui(self):
        """Set up the user interface."""
        self._setup_header()
        self._setup_main_content()
        self._setup_status_bar()

    def _setup_header(self):
        """Create the header with controls."""
        header_frame = ctk.CTkFrame(self.root, height=80, fg_color=Theme.PRIMARY)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)

        # Title section with icon and logo
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Game icon (Pepe)
        icon_image = icon_manager.create_ctk_image((40, 40), maintain_aspect=True)
        if icon_image:
            icon_label = ctk.CTkLabel(
                title_frame,
                image=icon_image,
                text=""
            )
            icon_label.grid(row=0, column=0, padx=(0, 15), pady=5)

        # Game logo (Ready Set Bet text image)
        logo_image = icon_manager.create_logo_image(target_height=35)
        if logo_image:
            logo_label = ctk.CTkLabel(
                title_frame,
                image=logo_image,
                text=""
            )
            logo_label.grid(row=0, column=1, pady=5)
        else:
            # Fallback to text if logo image not found
            title_label = ctk.CTkLabel(
                title_frame,
                text="Ready Set Bet",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=Theme.WIN
            )
            title_label.grid(row=0, column=1, pady=5)

        # Race info
        self.race_label = ctk.CTkLabel(
            header_frame,
            text=f"Race: {self.game_state.current_race}/{MAX_RACES}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.race_label.grid(row=0, column=1, padx=20, pady=20)

        # Control buttons
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.grid(row=0, column=2, padx=20, pady=20, sticky="e")

        # Create and store button references
        button_configs = [
            ("add_player", "👤 Add Player", self.add_player, Theme.ACCENT),
            ("start_race", "🚦 Start Race", self.start_race, Theme.SUCCESS),
            ("end_race", "🏁 End Race", self.end_race, Theme.WARNING),
            ("next_race", "⏭️ Next Race", self.next_race, Theme.ACCENT),
            ("reset_game", "🔄 Reset Game", self.reset_game, Theme.DANGER)
        ]

        for i, (key, text, command, color) in enumerate(button_configs):
            btn = ctk.CTkButton(
                controls_frame,
                text=text,
                command=command,
                fg_color=color,
                font=ctk.CTkFont(size=12),
                width=100,
                height=32
            )
            btn.grid(row=0, column=i, padx=5)
            self.control_buttons[key] = btn

    def _setup_main_content(self):
        """Set up the main content area."""
        # Left sidebar for players and results
        sidebar = ctk.CTkFrame(self.root, width=300, fg_color=Theme.CARD)
        sidebar.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        sidebar.grid_rowconfigure(1, weight=1)

        # Players section
        players_label = ctk.CTkLabel(
            sidebar,
            text="🏇 Players",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        players_label.grid(row=0, column=0, pady=10, sticky="ew")

        # Players listbox (using textbox for modern look)
        self.players_text = ctk.CTkTextbox(
            sidebar,
            font=ctk.CTkFont(size=12),
            fg_color=Theme.SURFACE,
            height=200
        )
        self.players_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Results section
        results_label = ctk.CTkLabel(
            sidebar,
            text="📊 Race Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        results_label.grid(row=2, column=0, pady=10, sticky="ew")

        self.results_text = ctk.CTkTextbox(
            sidebar,
            font=ctk.CTkFont(size=10),
            fg_color=Theme.SURFACE
        )
        self.results_text.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Main betting area
        self.betting_frame = ctk.CTkFrame(self.root, fg_color=Theme.SURFACE)
        self.betting_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))

        # Initialize the modern betting board
        self.betting_board = ModernBettingBoard(
            self.betting_frame,
            self.on_standard_bet,
            self.on_special_bet,
            self.on_prop_bet,
            self.on_exotic_bet
        )

        self.betting_board.set_game_state(self.game_state)
        self.betting_board.set_main_app_callback(self._update_button_states)
        self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
        self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
        self.betting_board.set_betting_enabled(False)

    def _setup_status_bar(self):
        """Set up the modern status bar."""
        status_frame = ctk.CTkFrame(self.root, height=40, fg_color=Theme.PRIMARY)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))

        self.status_var = ctk.StringVar()
        self.status_var.set("🚀 Ready to start - Add players to begin")

        status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        status_label.pack(side="left", padx=15, pady=10)

    # Event handlers for betting actions
    def on_standard_bet(self, horse: str, bet_type: str, multiplier: int, penalty: int, row: int, col: int):
        """Handle standard bet placement with modern dialog."""
        if not self._validate_betting():
            return

        spot_key = f"{horse}_{bet_type}_{row}_{col}"
        if spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error", f"This betting spot is already taken by {self.game_state.locked_spots[spot_key]}!")
            return

        dialog = ModernStandardBetDialog(self.root, self.game_state.players, horse, bet_type, multiplier, penalty)
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
                self._update_displays()
                self._update_button_states()
                self.status_var.set(f"✅ {result['player']} placed ${result['token_value']} token on Horse {horse} to {bet_type}")

    def on_special_bet(self, bet_name: str, multiplier: int):
        """Handle special bet placement."""
        if not self._validate_betting():
            return

        special_spot_key = f"special_{bet_name}"
        if special_spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error", f"This special bet is already taken!")
            return

        dialog = ModernSpecialBetDialog(self.root, self.game_state.players, bet_name, multiplier)
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
                self.betting_board.update_special_bet_appearance(bet_name, result["player"])
                self._update_displays()
                self._update_button_states()
                self.status_var.set(f"✅ {result['player']} placed special bet: {bet_name}")

    def on_prop_bet(self, prop_bet: dict):
        """Handle prop bet placement."""
        if not self._validate_betting():
            return

        prop_spot_key = f"prop_{prop_bet['id']}"
        if prop_spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error", f"This prop bet is already taken!")
            return

        dialog = ModernPropBetDialog(self.root, self.game_state.players, prop_bet)
        result = dialog.show()

        if result:
            bet = Bet(
                player=result["player"],
                horse="Prop",
                bet_type=prop_bet["description"],
                multiplier=prop_bet["multiplier"],
                penalty=prop_bet["penalty"],
                token_value=result["token_value"],
                spot_key=prop_spot_key,
                prop_bet_id=prop_bet["id"]
            )

            if self.game_state.place_bet(bet):
                self.betting_board.update_prop_bet_appearance(prop_bet["id"], result["player"])
                self._update_displays()
                self._update_button_states()
                self.status_var.set(f"✅ {result['player']} placed prop bet")

    def on_exotic_bet(self, exotic_finish: dict):
        """Handle exotic finish bet placement."""
        if not self._validate_betting():
            return

        # Check how many players have already bet on this exotic finish
        current_bets_on_exotic = [bet for bet in self.game_state.current_bets.values()
                                  if bet.is_exotic_bet() and bet.exotic_finish_id == exotic_finish['id']]

        if len(current_bets_on_exotic) >= 3:
            messagebox.showerror("Error", "This exotic finish already has 3 players betting on it!")
            return

        dialog = ModernExoticFinishDialog(self.root, self.game_state.players, exotic_finish)
        result = dialog.show()

        if result:
            player_exotic_spot_key = f"exotic_{exotic_finish['id']}_{result['player']}"

            bet = Bet(
                player=result["player"],
                horse="Exotic",
                bet_type=exotic_finish["name"],
                multiplier=exotic_finish["multiplier"],
                penalty=exotic_finish["penalty"],
                token_value=result["token_value"],
                spot_key=player_exotic_spot_key,
                exotic_finish_id=exotic_finish["id"]
            )

            if self.game_state.place_bet(bet):
                all_players_on_exotic = [bet.player for bet in self.game_state.current_bets.values()
                                       if bet.is_exotic_bet() and bet.exotic_finish_id == exotic_finish['id']]
                self.betting_board.update_exotic_finish_appearance(exotic_finish["id"], all_players_on_exotic)
                self._update_displays()
                self._update_button_states()
                self.status_var.set(f"✅ {result['player']} placed exotic finish bet")

    def _validate_betting(self) -> bool:
        """Validate that betting is allowed."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return False
        if not self.game_state.race_active:
            messagebox.showerror("Error", "Race must be started before placing bets!")
            return False
        return True

    # Game control methods
    def add_player(self):
        """Add a new player using modern dialog."""
        print("DEBUG: add_player called")  # Debug print
        try:
            dialog = ModernAddPlayerDialog(self.root, list(self.game_state.players.keys()))
            print("DEBUG: Dialog created")  # Debug print
            result = dialog.show()
            print(f"DEBUG: Dialog result: {result}")  # Debug print

            if result:
                success = self.game_state.add_player(result)
                print(f"DEBUG: Player added: {success}")  # Debug print
                if success:
                    self._update_player_display()
                    self._update_button_states()
                    self.status_var.set(f"✅ Added player: {result}")
                else:
                    print("DEBUG: Failed to add player to game state")
        except Exception as e:
            print(f"DEBUG: Error in add_player: {e}")
            import traceback
            traceback.print_exc()

    def start_race(self):
        """Start a race."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        self.game_state.start_race()
        self.betting_board.set_betting_enabled(True)
        self._update_button_states()
        self.status_var.set("🏁 Race in progress - Place your bets!")
        self._log_message("🚦 Race started - Betting is now open!")

    def end_race(self):
        """End the current race."""
        if not self.game_state.current_bets:
            messagebox.showerror("Error", "No bets placed!")
            return

        self.game_state.end_race()
        self.betting_board.set_betting_enabled(False)

        try:
            # Show race results dialog
            print("DEBUG: Opening race results dialog")  # Debug print
            dialog = ModernRaceResultsDialog(
                self.root,
                HORSES,
                self.game_state.current_prop_bets,
                self.game_state.current_exotic_finishes,
                self.game_state.current_bets
            )

            result = dialog.show()
            print(f"DEBUG: Dialog returned result: {result}")  # Debug print

            if result:
                print("DEBUG: Processing race results")  # Debug print
                winners, losers = self.game_logic.process_race_results(
                    result["win"],
                    result["place"],
                    result["show"],
                    result.get("prop_results", {}),
                    result.get("exotic_results", {})
                )

                self._log_race_results(
                    result["win"],
                    result["place"],
                    result["show"],
                    winners,
                    losers,
                    result.get("prop_results", {}),
                    result.get("exotic_results", {})
                )

                # Clear bets and reset board
                self.game_state.current_bets.clear()
                self.game_state.locked_spots.clear()
                self.betting_board.reset_all_buttons()
                self.betting_board.reset_prop_buttons_to_purple(self.game_state.current_prop_bets)
                self.betting_board.reset_exotic_finishes_to_orange(self.game_state.current_exotic_finishes)
                self.betting_board.set_betting_enabled(False)

                self._update_displays()
                self._update_button_states()
                self.status_var.set(f"🏁 Race {self.game_state.current_race} completed - Click 'Next Race' to continue!")
            else:
                print("DEBUG: Dialog was cancelled, re-enabling betting")  # Debug print
                # User cancelled - re-enable betting
                self.game_state.race_active = True  # Reset race state
                self.betting_board.set_betting_enabled(True)
                self._update_button_states()
                self.status_var.set("🏁 Race still in progress - Enter results to complete!")

        except Exception as e:
            print(f"DEBUG: Error in end_race: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            # On error, re-enable betting
            self.game_state.race_active = True
            self.betting_board.set_betting_enabled(True)
            self._update_button_states()
            messagebox.showerror("Error", f"Failed to process race results: {e}")

    def next_race(self):
        """Advance to the next race."""
        if self.game_logic.is_game_complete():
            self._end_game()
            return

        self.game_state.next_race()
        self.betting_board.reset_all_buttons()
        self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
        self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
        self.betting_board.set_betting_enabled(False)
        self._update_displays()
        self._update_race_display()
        self._update_button_states()
        self.status_var.set(f"🏁 Race {self.game_state.current_race} ready!")

    def reset_game(self):
        """Reset the entire game."""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            self.game_state.reset_game()
            self.betting_board.reset_all_buttons()
            self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
            self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
            self.betting_board.set_betting_enabled(False)
            self._update_displays()
            self._update_race_display()
            self._update_button_states()
            self.results_text.delete("1.0", "end")
            self.status_var.set("🔄 Game reset - Add players and start racing!")

    def _end_game(self):
        """End the game and show final results."""
        standings = self.game_logic.get_final_standings()

        result_text = "🏆 FINAL RESULTS:\n\n"
        for i, (name, money) in enumerate(standings):
            emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏇"
            result_text += f"{emoji} {i + 1}. {name}: ${money}\n"

        self._log_message(result_text)
        self._update_button_states()
        messagebox.showinfo("Game Over", result_text)

    # Utility methods
    def _update_displays(self):
        """Update all display components."""
        self._update_player_display()
        self.betting_board.update_bets_display(self.game_state.current_bets)

    def _update_player_display(self):
        """Update the modern player list display."""
        self.players_text.delete("1.0", "end")

        if not self.game_state.players:
            self.players_text.insert("1.0", "No players added yet.\n\nClick 'Add Player' to start!")
            return

        for player in self.game_state.players.values():
            tokens_available = []
            for value in ["5", "3", "2", "1"]:
                available = player.get_available_tokens(value)
                total = player.tokens[value]
                tokens_available.append(f"${value}: {available}/{total}")

            tokens_str = " | ".join(tokens_available)

            player_info = (
                f"🏇 {player.name}\n"
                f"💰 Money: ${player.money}\n"
                f"🎫 Tokens: {tokens_str}\n"
                f"{'─' * 30}\n\n"
            )
            self.players_text.insert("end", player_info)

    def _update_race_display(self):
        """Update the race display."""
        self.race_label.configure(text=f"Race: {self.game_state.current_race}/{MAX_RACES}")

    def _update_button_states(self):
        """Update control button states based on game state."""
        states = self._get_button_states()

        for button_key, (enabled, text, color) in states.items():
            if button_key in self.control_buttons:
                button = self.control_buttons[button_key]
                button.configure(
                    state="normal" if enabled else "disabled",
                    text=text,
                    fg_color=color if enabled else Theme.DISABLED
                )

    def _get_button_states(self) -> Dict[str, tuple]:
        """Calculate button states."""
        return {
            "add_player": (
                not self.game_state.race_active,
                "👤 Add Player" + (" (Race Active)" if self.game_state.race_active else ""),
                Theme.ACCENT
            ),
            "start_race": (
                not self.game_state.race_active and bool(self.game_state.players),
                "🚦 Start Race" + self._get_start_race_suffix(),
                Theme.SUCCESS
            ),
            "end_race": (
                self.game_state.race_active and bool(self.game_state.current_bets),
                "🏁 End Race" + self._get_end_race_suffix(),
                Theme.WARNING
            ),
            "next_race": (
                self._can_advance_race(),
                "⏭️ Next Race" + self._get_next_race_suffix(),
                Theme.ACCENT
            ),
            "reset_game": (
                True,
                "🔄 Reset Game",
                Theme.DANGER
            )
        }

    def _get_start_race_suffix(self) -> str:
        if self.game_state.race_active:
            return " (Active)"
        elif not self.game_state.players:
            return " (No Players)"
        return ""

    def _get_end_race_suffix(self) -> str:
        if not self.game_state.race_active:
            return " (Not Started)"
        elif not self.game_state.current_bets:
            return " (No Bets)"
        return ""

    def _get_next_race_suffix(self) -> str:
        if self.game_state.race_active:
            return " (Race Active)"
        elif self.game_state.current_race > MAX_RACES:
            return " (Game Over)"
        elif self.game_state.race_results is None and self.game_state.current_race > 1:
            return " (Complete Current)"
        return ""

    def _can_advance_race(self) -> bool:
        return (
            not self.game_state.race_active and
            self.game_state.current_race <= MAX_RACES and
            (self.game_state.race_results is not None or self.game_state.current_race == 1)
        )

    def _log_message(self, message: str):
        """Log a message to the results display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert("end", f"[{timestamp}] {message}\n")

    def _log_race_results(self, win_horses, place_horses, show_horses, winners, losers, prop_results, exotic_results):
        """Log race results and payouts."""
        self._log_message(f"🏁 Race {self.game_state.current_race} Results:")
        self._log_message(f"🥇 WIN: Horses {', '.join(map(str, win_horses))}")
        self._log_message(f"🥈 PLACE: Horses {', '.join(map(str, place_horses))}")
        self._log_message(f"🥉 SHOW: Horses {', '.join(map(str, show_horses))}")

        # Log prop bet results
        if prop_results:
            self._log_message("🎯 Prop Bet Results:")
            for prop_id, won in prop_results.items():
                prop_bet = next((p for p in self.game_state.current_prop_bets if p["id"] == prop_id), None)
                if prop_bet:
                    result_text = "✅ WON" if won else "❌ LOST"
                    self._log_message(f"  {prop_bet['description']}: {result_text}")

        # Log exotic finish results
        if exotic_results:
            self._log_message("⭐ Exotic Finish Results:")
            for exotic_id, won in exotic_results.items():
                exotic_finish = next((ef for ef in self.game_state.current_exotic_finishes if ef["id"] == exotic_id), None)
                if exotic_finish:
                    result_text = "✅ WON" if won else "❌ LOST"
                    self._log_message(f"  {exotic_finish['name']}: {result_text}")

        if winners:
            self._log_message("💰 Winners:")
            for winner in winners:
                self._log_message(f"  {winner}")

        if losers:
            self._log_message("💸 Losers (penalties applied):")
            for loser in losers:
                self._log_message(f"  {loser}")

        if not winners and not losers:
            self._log_message("❓ No bets placed this race!")