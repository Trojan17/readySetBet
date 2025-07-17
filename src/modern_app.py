"""Modern main application class for Ready Set Bet using CustomTkinter."""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from .icon_utils import icon_manager
from .models import GameState, Bet
from .game_logic import GameLogic
from .modern_ui_components import ModernBettingBoard
from .modern_dialogs import (
    ModernStandardBetDialog,
    ModernSpecialBetDialog,
    ModernPropBetDialog,
    ModernExoticFinishDialog,
    ModernAddPlayerDialog,
    ModernRaceResultsDialog
)
from .constants import HORSES, MAX_RACES

# Modern color scheme for Ready Set Bet
RACING_COLORS = {
    "primary": "#1f2937",      # Dark gray
    "secondary": "#374151",    # Medium gray
    "accent": "#3b82f6",       # Blue
    "success": "#10b981",      # Green
    "warning": "#f59e0b",      # Amber
    "danger": "#ef4444",       # Red
    "surface": "#111827",      # Very dark gray
    "card": "#1f2937",         # Card background

    # Betting colors (modern versions)
    "show": "#cd7f32",    # Bronze
    "place": "#c0c0c0",   # Silver
    "win": "#ffd700",     # Gold
    "locked": "#6b7280",  # Gray

    # Special bet colors
    "blue_bet": "#3b82f6",
    "orange_bet": "#f97316",
    "red_bet": "#ef4444",
    "black_bet": "#6b7280",

    # Prop and exotic
    "prop": "#8b5cf6",     # Purple
    "exotic": "#0891b2",   # Orange

    # Button states
    "disabled": "#4b5563",  # Dark gray for disabled buttons
}


class ModernReadySetBetApp:
    """Modern main application using CustomTkinter."""

    def __init__(self, root):
        self.root = root
        self.root.title("🏇 Ready Set Bet - Modern Betting Board")
        self.root.geometry("1400x900")

        # Configure modern appearance
        self.root.configure(fg_color=RACING_COLORS["surface"])

        # Initialize game state and logic
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

        # Control buttons - store references for state management
        self.add_player_btn = None
        self.start_race_btn = None
        self.end_race_btn = None
        self.next_race_btn = None
        self.reset_game_btn = None

        self.setup_ui()
        self.update_button_states()  # Set initial button states

    def setup_ui(self):
        """Set up the modern user interface."""
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        # Setup UI sections
        self._setup_header()
        self._setup_main_content()
        self._setup_status_bar()

    def _setup_header(self):
        """Set up the modern header with controls."""
        header_frame = ctk.CTkFrame(self.root, height=80, fg_color=RACING_COLORS["primary"])
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
        logo_image = icon_manager.create_logo_image(target_height=35)  # Adjust height as needed
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
                text_color=RACING_COLORS["win"]
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
        self.add_player_btn = ctk.CTkButton(
            controls_frame,
            text="👤 Add Player",
            command=self.add_player,
            fg_color=RACING_COLORS["accent"],
            font=ctk.CTkFont(size=12),
            width=100,
            height=32
        )
        self.add_player_btn.grid(row=0, column=0, padx=5)

        self.start_race_btn = ctk.CTkButton(
            controls_frame,
            text="🚦 Start Race",
            command=self.start_race,
            fg_color=RACING_COLORS["success"],
            font=ctk.CTkFont(size=12),
            width=100,
            height=32
        )
        self.start_race_btn.grid(row=0, column=1, padx=5)

        self.end_race_btn = ctk.CTkButton(
            controls_frame,
            text="🏁 End Race",
            command=self.end_race,
            fg_color=RACING_COLORS["warning"],
            font=ctk.CTkFont(size=12),
            width=100,
            height=32
        )
        self.end_race_btn.grid(row=0, column=2, padx=5)

        self.next_race_btn = ctk.CTkButton(
            controls_frame,
            text="⏭️ Next Race",
            command=self.next_race,
            fg_color=RACING_COLORS["accent"],
            font=ctk.CTkFont(size=12),
            width=100,
            height=32
        )
        self.next_race_btn.grid(row=0, column=3, padx=5)

        self.reset_game_btn = ctk.CTkButton(
            controls_frame,
            text="🔄 Reset Game",
            command=self.reset_game,
            fg_color=RACING_COLORS["danger"],
            font=ctk.CTkFont(size=12),
            width=100,
            height=32
        )
        self.reset_game_btn.grid(row=0, column=4, padx=5)

    def update_button_states(self):
        """Update the state of control buttons based on current game state."""
        # Add Player: Only enabled when race is not active
        if self.game_state.race_active:
            self.add_player_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text="👤 Add Player (Race Active)"
            )
        else:
            self.add_player_btn.configure(
                state="normal",
                fg_color=RACING_COLORS["accent"],
                text="👤 Add Player"
            )

        # Start Race: Only enabled when race is not active and there are players
        if self.game_state.race_active or not self.game_state.players:
            disabled_text = "🚦 Start Race"
            if self.game_state.race_active:
                disabled_text += " (Active)"
            elif not self.game_state.players:
                disabled_text += " (No Players)"

            self.start_race_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text=disabled_text
            )
        else:
            self.start_race_btn.configure(
                state="normal",
                fg_color=RACING_COLORS["success"],
                text="🚦 Start Race"
            )

        # End Race: Only enabled when race is active and there are bets
        if not self.game_state.race_active or not self.game_state.current_bets:
            disabled_text = "🏁 End Race"
            if not self.game_state.race_active:
                disabled_text += " (Not Started)"
            elif not self.game_state.current_bets:
                disabled_text += " (No Bets)"

            self.end_race_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text=disabled_text
            )
        else:
            self.end_race_btn.configure(
                state="normal",
                fg_color=RACING_COLORS["warning"],
                text="🏁 End Race"
            )

        # Next Race: Only enabled when race is not active and not at the last race
        # Also needs to have completed the current race (race_results exists)
        can_advance = (
            not self.game_state.race_active and
            self.game_state.current_race <= MAX_RACES and
            (self.game_state.race_results is not None or self.game_state.current_race == 1)
        )

        if not can_advance:
            disabled_text = "⏭️ Next Race"
            if self.game_state.race_active:
                disabled_text += " (Race Active)"
            elif self.game_state.current_race > MAX_RACES:
                disabled_text += " (Game Over)"
            elif self.game_state.race_results is None and self.game_state.current_race > 1:
                disabled_text += " (Complete Current)"

            self.next_race_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text=disabled_text
            )
        else:
            if self.game_state.current_race > MAX_RACES:
                self.next_race_btn.configure(
                    state="disabled",
                    fg_color=RACING_COLORS["disabled"],
                    text="⏭️ Game Complete"
                )
            else:
                self.next_race_btn.configure(
                    state="normal",
                    fg_color=RACING_COLORS["accent"],
                    text="⏭️ Next Race"
                )

        # Reset Game: Always enabled
        self.reset_game_btn.configure(
            state="normal",
            fg_color=RACING_COLORS["danger"],
            text="🔄 Reset Game"
        )

    def update_button_states(self):
        """Update the state of control buttons based on current game state."""
        # Add Player: Only enabled when race is not active
        if self.game_state.race_active:
            self.add_player_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text="👤 Add Player (Race Active)"
            )
        else:
            self.add_player_btn.configure(
                state="normal",
                fg_color=RACING_COLORS["accent"],
                text="👤 Add Player"
            )

        # Start Race: Only enabled when race is not active and there are players
        if self.game_state.race_active or not self.game_state.players:
            disabled_text = "🚦 Start Race"
            if self.game_state.race_active:
                disabled_text += " (Active)"
            elif not self.game_state.players:
                disabled_text += " (No Players)"

            self.start_race_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text=disabled_text
            )
        else:
            self.start_race_btn.configure(
                state="normal",
                fg_color=RACING_COLORS["success"],
                text="🚦 Start Race"
            )

        # End Race: Only enabled when race is active and there are bets
        if not self.game_state.race_active or not self.game_state.current_bets:
            disabled_text = "🏁 End Race"
            if not self.game_state.race_active:
                disabled_text += " (Not Started)"
            elif not self.game_state.current_bets:
                disabled_text += " (No Bets)"

            self.end_race_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text=disabled_text
            )
        else:
            self.end_race_btn.configure(
                state="normal",
                fg_color=RACING_COLORS["warning"],
                text="🏁 End Race"
            )

        # Next Race: Only enabled when race is not active and not at the last race
        # Also needs to have completed the current race (race_results exists)
        can_advance = (
            not self.game_state.race_active and
            self.game_state.current_race <= MAX_RACES and
            (self.game_state.race_results is not None or self.game_state.current_race == 1)
        )

        if not can_advance:
            disabled_text = "⏭️ Next Race"
            if self.game_state.race_active:
                disabled_text += " (Race Active)"
            elif self.game_state.current_race > MAX_RACES:
                disabled_text += " (Game Over)"
            elif self.game_state.race_results is None and self.game_state.current_race > 1:
                disabled_text += " (Complete Current)"

            self.next_race_btn.configure(
                state="disabled",
                fg_color=RACING_COLORS["disabled"],
                text=disabled_text
            )
        else:
            if self.game_state.current_race > MAX_RACES:
                self.next_race_btn.configure(
                    state="disabled",
                    fg_color=RACING_COLORS["disabled"],
                    text="⏭️ Game Complete"
                )
            else:
                self.next_race_btn.configure(
                    state="normal",
                    fg_color=RACING_COLORS["accent"],
                    text="⏭️ Next Race"
                )

        # Reset Game: Always enabled
        self.reset_game_btn.configure(
            state="normal",
            fg_color=RACING_COLORS["danger"],
            text="🔄 Reset Game"
        )

    def _setup_main_content(self):
        """Set up the main content area."""
        # Left sidebar for players and results
        sidebar = ctk.CTkFrame(self.root, width=300, fg_color=RACING_COLORS["card"])
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
            font=ctk.CTkFont(size=12),  # CHANGE: was size=14, now size=12
            fg_color=RACING_COLORS["surface"],
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
            fg_color=RACING_COLORS["surface"]
        )
        self.results_text.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="nsew")

        # Main betting area
        self.betting_frame = ctk.CTkFrame(self.root, fg_color=RACING_COLORS["surface"])
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
        self.betting_board.set_main_app_callback(self.update_button_states)
        self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
        self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
        self.betting_board.set_betting_enabled(False)

    def _setup_status_bar(self):
        """Set up the modern status bar."""
        status_frame = ctk.CTkFrame(self.root, height=40, fg_color=RACING_COLORS["primary"])
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
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        if not self.game_state.race_active:
            messagebox.showerror("Error", "Race must be started before placing bets!")
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
                self.update_displays()
                self.update_button_states()  # Update button states after placing bet
                self.status_var.set(f"✅ {result['player']} placed ${result['token_value']} token on Horse {horse} to {bet_type}")

    def on_special_bet(self, bet_name: str, multiplier: int):
        """Handle special bet placement."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        if not self.game_state.race_active:
            messagebox.showerror("Error", "Race must be started before placing bets!")
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
                self.update_displays()
                self.update_button_states()  # Update button states after placing bet
                self.status_var.set(f"✅ {result['player']} placed special bet: {bet_name}")

    def on_prop_bet(self, prop_bet: dict):
        """Handle prop bet placement."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        if not self.game_state.race_active:
            messagebox.showerror("Error", "Race must be started before placing bets!")
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
                self.update_displays()
                self.update_button_states()  # Update button states after placing bet
                self.status_var.set(f"✅ {result['player']} placed prop bet")

    def on_exotic_bet(self, exotic_finish: dict):
        """Handle exotic finish bet placement."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        if not self.game_state.race_active:
            messagebox.showerror("Error", "Race must be started before placing bets!")
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
                self.update_displays()
                self.update_button_states()  # Update button states after placing bet
                self.status_var.set(f"✅ {result['player']} placed exotic finish bet")

    # Game control methods
    def add_player(self):
        """Add a new player using modern dialog."""
        dialog = ModernAddPlayerDialog(self.root, list(self.game_state.players.keys()))
        if dialog.result:
            self.game_state.add_player(dialog.result)
            self.update_player_display()
            self.update_button_states()  # Update button states after adding player
            self.status_var.set(f"✅ Added player: {dialog.result}")

    def start_race(self):
        """Start a race."""
        if not self.game_state.players:
            messagebox.showerror("Error", "No players added!")
            return

        self.game_state.start_race()
        self.betting_board.set_betting_enabled(True)
        self.update_button_states()  # Update button states after starting race
        self.status_var.set("🏁 Race in progress - Place your bets!")
        self.log_message("🚦 Race started - Betting is now open!")

    def end_race(self):
        """End the current race."""
        if not self.game_state.current_bets:
            messagebox.showerror("Error", "No bets placed!")
            return

        self.game_state.end_race()
        self.betting_board.set_betting_enabled(False)

        # Show race results dialog
        dialog = ModernRaceResultsDialog(
            self.root,
            HORSES,
            self.game_state.current_prop_bets,
            self.game_state.current_exotic_finishes,
            self.game_state.current_bets
        )

        if dialog.result:
            winners, losers = self.game_logic.process_race_results(
                dialog.result["win"],
                dialog.result["place"],
                dialog.result["show"],
                dialog.result.get("prop_results", {}),
                dialog.result.get("exotic_results", {})
            )

            self.log_race_results(
                dialog.result["win"],
                dialog.result["place"],
                dialog.result["show"],
                winners,
                losers,
                dialog.result.get("prop_results", {}),
                dialog.result.get("exotic_results", {})
            )

            # Clear bets and reset board
            self.game_state.current_bets.clear()
            self.game_state.locked_spots.clear()
            self.betting_board.reset_all_buttons()
            self.betting_board.reset_prop_buttons_to_purple(self.game_state.current_prop_bets)
            self.betting_board.reset_exotic_finishes_to_orange(self.game_state.current_exotic_finishes)
            self.betting_board.set_betting_enabled(False)

            self.update_displays()
            self.update_button_states()  # Update button states after ending race
            self.status_var.set(f"🏁 Race {self.game_state.current_race} completed - Click 'Next Race' to continue!")
        else:
            # User cancelled - re-enable betting
            self.betting_board.set_betting_enabled(True)
            self.update_button_states()  # Restore button states
            self.status_var.set("🏁 Race still in progress - Enter results to complete!")

    def next_race(self):
        """Advance to the next race."""
        if self.game_logic.is_game_complete():
            self.end_game()
            return

        self.game_state.next_race()
        self.betting_board.reset_all_buttons()
        self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
        self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
        self.betting_board.set_betting_enabled(False)
        self.update_displays()
        self.update_race_display()
        self.update_button_states()  # Update button states after advancing race
        self.status_var.set(f"🏁 Race {self.game_state.current_race} ready!")

    def reset_game(self):
        """Reset the entire game."""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            self.game_state.reset_game()
            self.betting_board.reset_all_buttons()
            self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
            self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
            self.betting_board.set_betting_enabled(False)
            self.update_displays()
            self.update_race_display()
            self.update_button_states()  # Update button states after reset
            self.results_text.delete("1.0", "end")
            self.status_var.set("🔄 Game reset - Add players and start racing!")

    def end_game(self):
        """End the game and show final results."""
        standings = self.game_logic.get_final_standings()

        result_text = "🏆 FINAL RESULTS:\n\n"
        for i, (name, money) in enumerate(standings):
            emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "🏇"
            result_text += f"{emoji} {i + 1}. {name}: ${money}\n"

        self.log_message(result_text)
        self.update_button_states()  # Update button states for game over
        messagebox.showinfo("Game Over", result_text)

    # Utility methods
    def update_displays(self):
        """Update all display components."""
        self.update_player_display()
        self.betting_board.update_bets_display(self.game_state.current_bets)

    def update_player_display(self):
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

            # IMPROVED formatting with bigger spacing and clearer layout
            player_info = (
                f"🏇 {player.name}\n"
                f"💰 Money: ${player.money}\n"
                f"🎫 Tokens: {tokens_str}\n"
                f"{'─' * 30}\n\n"  # Add separator line
            )
            self.players_text.insert("end", player_info)

    def update_race_display(self):
        """Update the race display."""
        self.race_label.configure(text=f"Race: {self.game_state.current_race}/{MAX_RACES}")

    def log_message(self, message: str):
        """Log a message to the results display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.results_text.insert("end", f"[{timestamp}] {message}\n")

    def log_race_results(self, win_horses, place_horses, show_horses, winners, losers, prop_results, exotic_results):
        """Log race results and payouts."""
        self.log_message(f"🏁 Race {self.game_state.current_race} Results:")
        self.log_message(f"🥇 WIN: Horses {', '.join(map(str, win_horses))}")
        self.log_message(f"🥈 PLACE: Horses {', '.join(map(str, place_horses))}")
        self.log_message(f"🥉 SHOW: Horses {', '.join(map(str, show_horses))}")

        # Log prop bet results
        if prop_results:
            self.log_message("🎯 Prop Bet Results:")
            for prop_id, won in prop_results.items():
                prop_bet = next((p for p in self.game_state.current_prop_bets if p["id"] == prop_id), None)
                if prop_bet:
                    result_text = "✅ WON" if won else "❌ LOST"
                    self.log_message(f"  {prop_bet['description']}: {result_text}")

        # Log exotic finish results
        if exotic_results:
            self.log_message("⭐ Exotic Finish Results:")
            for exotic_id, won in exotic_results.items():
                exotic_finish = next((ef for ef in self.game_state.current_exotic_finishes if ef["id"] == exotic_id), None)
                if exotic_finish:
                    result_text = "✅ WON" if won else "❌ LOST"
                    self.log_message(f"  {exotic_finish['name']}: {result_text}")

        if winners:
            self.log_message("💰 Winners:")
            for winner in winners:
                self.log_message(f"  {winner}")

        if losers:
            self.log_message("💸 Losers (penalties applied):")
            for loser in losers:
                self.log_message(f"  {loser}")

        if not winners and not losers:
            self.log_message("❓ No bets placed this race!")