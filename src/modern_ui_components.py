"""Modern UI components for the Ready Set Bet application using CustomTkinter."""

import customtkinter as ctk
from typing import Dict, List, Callable
from .constants import HORSES, BETTING_GRID, SPECIAL_BETS, HORSE_COLORS

# Modern color scheme with better contrast
BETTING_COLORS = {
    "show": "#cd7f32",  # Bronze
    "place": "#c0c0c0",  # Silver
    "win": "#ffd700",  # Gold
    "locked": "#6b7280",  # Gray
    "hover_show": "#b8691a",
    "hover_place": "#a8a8a8",
    "hover_win": "#e6c200",

    "blue_bet": "#2563eb",    # More vibrant blue
    "orange_bet": "#ea580c",  # More vibrant orange
    "red_bet": "#dc2626",     # More vibrant red
    "black_bet": "#7c2d12",   # Dark gray

    "prop": "#7c3aed",     # More vibrant purple
    "exotic": "#0891b2",   # More vibrant orange
    "surface": "#111827",
    "card": "#1f2937",
    "text": "#ffffff",
    "text_dark": "#000000"
}


class ModernBettingBoard:
    """Modern betting board component using CustomTkinter."""

    def __init__(self, parent, on_standard_bet: Callable, on_special_bet: Callable,
                 on_prop_bet: Callable, on_exotic_bet: Callable):
        self.parent = parent
        self.on_standard_bet = on_standard_bet
        self.on_special_bet = on_special_bet
        self.on_prop_bet = on_prop_bet
        self.on_exotic_bet = on_exotic_bet

        # Storage for button references
        self.bet_buttons = {}
        self.special_bet_buttons = {}
        self.prop_bet_buttons = {}
        self.exotic_finish_buttons = {}

        # ADD: Storage for current bets and game state reference
        self.current_bets = {}
        self.game_state = None  # Will be set by the main app

        self.setup_board()

    def set_game_state(self, game_state):
        """Set reference to game state for bet management."""
        self.game_state = game_state

    def remove_selected_bet(self):
        """Remove the selected bet from the textbox."""
        if not self.game_state:
            return
        try:
            # Get current selection from textbox
            selection = self.bets_text.selection_get()
            if not selection:
                # No selection, try to get current line
                current_pos = self.bets_text.index("insert")
                line_start = current_pos.split('.')[0] + '.0'
                line_end = current_pos.split('.')[0] + '.end'
                selection = self.bets_text.get(line_start, line_end)

            if selection:
                # Find the bet by matching player and bet info
                for bet_id, bet in list(self.game_state.current_bets.items()):
                    if bet.player in selection:
                        # Remove the bet
                        if self.game_state.remove_bet(bet_id):
                            # Update the display
                            self.update_bets_display(self.game_state.current_bets)
                            # Reset button appearance
                            self._reset_bet_button(bet)
                            break

        except Exception as e:
            print(f"No bet selected or error removing bet: {e}")
    def setup_board(self):
        """Set up the modern betting board."""
        # Main container with scrollable frame
        self.main_container = ctk.CTkScrollableFrame(
            self.parent,
            fg_color=BETTING_COLORS["surface"],
            scrollbar_fg_color=BETTING_COLORS["card"]
        )
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure grid
        self.main_container.grid_columnconfigure(0, weight=1)

        # Setup sections
        self._setup_prop_bets()
        self._setup_special_bets()
        self._setup_exotic_finishes()
        self._setup_main_grid()
        self._setup_current_bets()

    def _setup_prop_bets(self):
        """Set up the modern prop bets section."""
        self.prop_frame = ctk.CTkFrame(self.main_container, fg_color=BETTING_COLORS["card"])
        self.prop_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        # Title
        prop_title = ctk.CTkLabel(
            self.prop_frame,
            text="🎯 PROPOSITION BETS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=BETTING_COLORS["prop"]
        )
        prop_title.pack(pady=(15, 10))

        # Container for prop bet buttons
        self.prop_buttons_frame = ctk.CTkFrame(self.prop_frame, fg_color="transparent")
        self.prop_buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

    def update_prop_bets(self, prop_bets: List[Dict]):
        """Update the prop bets display."""
        # Clear existing buttons
        for widget in self.prop_buttons_frame.winfo_children():
            widget.destroy()
        self.prop_bet_buttons.clear()

        if not prop_bets:
            no_props = ctk.CTkLabel(
                self.prop_buttons_frame,
                text="No proposition bets available",
                font=ctk.CTkFont(size=14),
                text_color="#9ca3af"
            )
            no_props.pack(pady=20)
            return

        # Configure grid for prop buttons
        self.prop_buttons_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        # Create prop bet buttons
        for i, prop_bet in enumerate(prop_bets):
            btn_text = f"{prop_bet['description']}\n💰 {prop_bet['multiplier']}x | 💸 -${prop_bet['penalty']}"

            btn = ctk.CTkButton(
                self.prop_buttons_frame,
                text=btn_text,
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=BETTING_COLORS["prop"],
                hover_color="#6d28d9",
                text_color="white",
                height=90,
                command=lambda pb=prop_bet: self.on_prop_bet(pb)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.prop_bet_buttons[prop_bet["id"]] = btn

    def _setup_special_bets(self):
        """Set up the modern special bets section."""
        special_frame = ctk.CTkFrame(self.main_container, fg_color=BETTING_COLORS["card"])
        special_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        # Title
        special_title = ctk.CTkLabel(
            special_frame,
            text="👑 SPECIAL RACING BETS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f59e0b"
        )
        special_title.pack(pady=(15, 10))

        # Special bet buttons container
        special_buttons_frame = ctk.CTkFrame(special_frame, fg_color="transparent")
        special_buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        special_buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Create special bet buttons
        color_map = {
            "blue": BETTING_COLORS["blue_bet"],
            "orange": BETTING_COLORS["orange_bet"],
            "red": BETTING_COLORS["red_bet"],
            "black": BETTING_COLORS["black_bet"]
        }

        for i, (name, payout, color) in enumerate(SPECIAL_BETS):
            if color in ["blue", "orange", "red"]:
                btn_text = f"{name}\n🏆 {payout} | 💸 -$1"
            else:
                btn_text = f"{name}\n🏆 {payout} | ✅ FREE"

            # Special handling for the 7th horse button
            if name == "7 Finishes 5th or Worse":
                def seventh_horse_click():
                    print("7 Finishes 5th or Worse button clicked!")
                    self.on_special_bet("7 Finishes 5th or Worse", 4)

                btn = ctk.CTkButton(
                    special_buttons_frame,
                    text=btn_text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    fg_color="#7c2d12",  # Dark brown
                    height=70,
                    command=seventh_horse_click
                )
            else:
                multiplier = int(payout.replace('x', ''))
                btn = ctk.CTkButton(
                    special_buttons_frame,
                    text=btn_text,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    fg_color=color_map[color],
                    height=70,
                    command=lambda n=name, m=multiplier: self.on_special_bet(n, m)
                )

            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.special_bet_buttons[name] = btn

    def _setup_exotic_finishes(self):
        """Set up the modern exotic finishes section."""
        self.exotic_container = ctk.CTkFrame(self.main_container, fg_color=BETTING_COLORS["card"])
        self.exotic_container.grid(row=2, column=0, sticky="ew", pady=(0, 15))

        # Title
        exotic_title = ctk.CTkLabel(
            self.exotic_container,
            text="⭐ EXOTIC FINISH BETS",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=BETTING_COLORS["exotic"]
        )
        exotic_title.pack(pady=(15, 10))

        # Container for exotic finish buttons
        self.exotic_frame = ctk.CTkFrame(self.exotic_container, fg_color="transparent")
        self.exotic_frame.pack(fill="x", padx=15, pady=(0, 15))

    def update_exotic_finishes(self, exotic_finishes: List[Dict]):
        """Update the exotic finishes display."""
        # Clear existing buttons
        for widget in self.exotic_frame.winfo_children():
            widget.destroy()
        self.exotic_finish_buttons.clear()

        if not exotic_finishes:
            no_exotic = ctk.CTkLabel(
                self.exotic_frame,
                text="No exotic finish bets available",
                font=ctk.CTkFont(size=14),
                text_color="#9ca3af"
            )
            no_exotic.pack(pady=20)
            return

        # Configure grid for exotic buttons
        cols = len(exotic_finishes)
        for i in range(cols):
            self.exotic_frame.grid_columnconfigure(i, weight=1)

        # Create exotic finish buttons
        for i, exotic_finish in enumerate(exotic_finishes):
            # CHANGE: Show FULL description without cutting it off
            btn_text = f"{exotic_finish['name']}\n{exotic_finish['description']}\n{exotic_finish['multiplier']}x | -${exotic_finish['penalty']}\nMax 3 players"

            btn = ctk.CTkButton(
                self.exotic_frame,
                text=btn_text,
                font=ctk.CTkFont(size=13, weight="bold"),  # Smaller font to fit more text
                fg_color=BETTING_COLORS["exotic"],
                hover_color="#0e7490",
                height=130,  # Taller to accommodate full text
                command=lambda ef=exotic_finish: self.on_exotic_bet(ef)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.exotic_finish_buttons[exotic_finish["id"]] = btn

    def _setup_main_grid(self):
        """Set up the main betting grid."""
        grid_container = ctk.CTkFrame(self.main_container, fg_color=BETTING_COLORS["card"])
        grid_container.grid(row=3, column=0, sticky="ew", pady=(0, 15))

        # Title
        grid_title = ctk.CTkLabel(
            grid_container,
            text="🏁 RACING ODDS BOARD",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ffd700"
        )
        grid_title.pack(pady=(15, 10))

        # Main grid frame
        self.grid_frame = ctk.CTkFrame(grid_container, fg_color=BETTING_COLORS["surface"])
        self.grid_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Configure grid columns
        for i in range(8):
            self.grid_frame.grid_columnconfigure(i, weight=1)

        # Headers
        self._setup_headers()

        # Betting buttons
        self._setup_betting_buttons()

    def _setup_headers(self):
        """Set up the betting grid headers."""
        headers = [
            ("🥉 SHOW", BETTING_COLORS["show"], 0, 2),
            ("🥈 PLACE", BETTING_COLORS["place"], 2, 2),
            ("🥇 WIN", BETTING_COLORS["win"], 4, 3)
        ]

        for text, color, col, span in headers:
            header = ctk.CTkLabel(
                self.grid_frame,
                text=text,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=color,
                text_color=BETTING_COLORS["text_dark"] if color == BETTING_COLORS["win"] else BETTING_COLORS["text"],
                height=45,
                corner_radius=8
            )
            header.grid(row=0, column=col, columnspan=span, padx=2, pady=2, sticky="ew")

    def _setup_betting_buttons(self):
        """Set up the betting buttons grid."""
        for horse_idx, horse in enumerate(HORSES):
            row = horse_idx + 1

            # Horse label with correct color from constants
            horse_color = HORSE_COLORS.get(horse, "#3b82f6")  # Use constants, default to blue

            horse_label = ctk.CTkLabel(
                self.grid_frame,
                text=f"🐎 {horse}",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=horse_color,  # Use color from constants
                text_color="white",
                height=35,
                corner_radius=6
            )
            horse_label.grid(row=row, column=7, padx=2, pady=2, sticky="ew")

            # Initialize button storage for this horse
            self.bet_buttons[horse] = {}

            # Betting spots
            horse_bets = BETTING_GRID[horse_idx]

            for col_idx, (multiplier, penalty) in enumerate(horse_bets):
                bet_type = "show" if col_idx < 2 else "place" if col_idx < 4 else "win"
                color = BETTING_COLORS[bet_type]
                hover_color = BETTING_COLORS[f"hover_{bet_type}"]
                text_color = "black" if bet_type == "win" else "white"

                # Button text
                if penalty > 0:
                    btn_text = f"{multiplier}x\n-${penalty}"
                else:
                    btn_text = f"{multiplier}x\nFREE"

                btn = ctk.CTkButton(
                    self.grid_frame,
                    text=btn_text,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=color,
                    hover_color=hover_color,
                    text_color=text_color,
                    height=35,
                    corner_radius=6,
                    command=lambda h=horse, t=bet_type, m=multiplier, p=penalty, r=row, c=col_idx:
                    self.on_standard_bet(h, t, m, p, r, c)
                )
                btn.grid(row=row, column=col_idx, padx=2, pady=2, sticky="ew")

                # Store button reference
                if bet_type not in self.bet_buttons[horse]:
                    self.bet_buttons[horse][bet_type] = []
                self.bet_buttons[horse][bet_type].append({
                    "button": btn,
                    "row": row,
                    "col": col_idx,
                    "multiplier": multiplier,
                    "penalty": penalty
                })

        # FIND the _setup_current_bets method in src/modern_ui_components.py and REPLACE it:

    def _setup_current_bets(self):
        """Set up the current bets display."""
        bets_container = ctk.CTkFrame(self.main_container, fg_color=BETTING_COLORS["card"])
        bets_container.grid(row=4, column=0, sticky="ew", pady=(0, 15))

        # Title
        bets_title = ctk.CTkLabel(
            bets_container,
            text="🎫 ACTIVE BETS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#10b981"
        )
        bets_title.pack(pady=(15, 10))

        # Scrollable frame for bet cards
        self.bets_scroll_frame = ctk.CTkScrollableFrame(
            bets_container,
            fg_color=BETTING_COLORS["surface"],
            height=200
        )
        self.bets_scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Clear All button
        button_frame = ctk.CTkFrame(bets_container, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🧹 Clear All Bets",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6b7280",
            hover_color="#4b5563",
            height=35,
            command=self.clear_all_bets
        )
        self.clear_btn.pack(fill="x")

    def update_bets_display(self, bets: Dict):
        """Update the current bets display with individual bet cards."""
        # Clear existing bet cards
        for widget in self.bets_scroll_frame.winfo_children():
            widget.destroy()

        if not bets:
            no_bets_label = ctk.CTkLabel(
                self.bets_scroll_frame,
                text="No active bets placed.\n\nStart betting to see them here!",
                font=ctk.CTkFont(size=12),
                text_color="#666666"
            )
            no_bets_label.pack(pady=20)
            return

        # Create individual bet cards
        for bet_id, bet in bets.items():
            self._create_bet_card(bet_id, bet)


    def update_button_appearance(self, horse: str, bet_type: str, row: int, col: int, player: str):
        """Update button to show it's locked by a player."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]

                    new_text = f"{multiplier}x\n🏇 {player[:6]}"
                    button.configure(
                        text=new_text,
                        fg_color=BETTING_COLORS["locked"],
                        hover_color=BETTING_COLORS["locked"],
                        text_color="white",
                        state="disabled"
                    )
                    break

    def update_special_bet_appearance(self, bet_name: str, player: str):
        """Update special bet button appearance."""
        if bet_name in self.special_bet_buttons:
            button = self.special_bet_buttons[bet_name]
            current_text = button.cget("text")
            lines = current_text.split('\n')
            if len(lines) >= 2:
                new_text = f"{lines[0]}\n{lines[1]}\n🏇 {player[:8]}"
            else:
                new_text = f"{current_text}\n🏇 {player[:8]}"

            button.configure(
                text=new_text,
                fg_color=BETTING_COLORS["locked"],
                hover_color=BETTING_COLORS["locked"],
                text_color="white",
                state="disabled"
            )

    def update_prop_bet_appearance(self, prop_bet_id: int, player: str):
        """Update prop bet button appearance."""
        if prop_bet_id in self.prop_bet_buttons:
            button = self.prop_bet_buttons[prop_bet_id]
            current_text = button.cget("text")
            lines = current_text.split('\n')
            if len(lines) >= 2:
                new_text = f"{lines[0]}\n{lines[1]}\n🏇 {player[:8]}"
            else:
                new_text = f"{current_text}\n🏇 {player[:8]}"

            button.configure(
                text=new_text,
                fg_color=BETTING_COLORS["locked"],
                hover_color=BETTING_COLORS["locked"],
                text_color="white",
                state="disabled"
            )

    def update_exotic_finish_appearance(self, exotic_finish_id: int, players: List[str]):
        """Update exotic finish button appearance."""
        if exotic_finish_id in self.exotic_finish_buttons:
            button = self.exotic_finish_buttons[exotic_finish_id]
            current_text = button.cget("text")
            lines = current_text.split('\n')

            # Keep first 3 lines, replace player info
            if len(lines) >= 3:
                player_text = ", ".join([f"🏇 {p[:6]}" for p in players])
                new_text = f"{lines[0]}\n{lines[1]}\n{lines[2]}\n{player_text}"
            else:
                player_text = ", ".join([f"🏇 {p[:6]}" for p in players])
                new_text = f"{current_text}\n{player_text}"

            # Lock if 3 players
            if len(players) >= 3:
                button.configure(
                    text=new_text,
                    fg_color=BETTING_COLORS["locked"],
                    hover_color=BETTING_COLORS["locked"],
                    text_color="white",
                    state="disabled"
                )
            else:
                button.configure(text=new_text, text_color="white")

    def set_betting_enabled(self, enabled: bool):
        """Enable or disable all betting buttons."""
        # Standard betting buttons
        for horse in self.bet_buttons:
            for bet_type in self.bet_buttons[horse]:
                for btn_info in self.bet_buttons[horse][bet_type]:
                    button = btn_info["button"]
                    if enabled:
                        if button.cget("fg_color") != BETTING_COLORS["locked"]:
                            button.configure(state="normal")
                    else:
                        button.configure(state="disabled")

        # Special bet buttons - MAKE SURE all are handled
        for button in self.special_bet_buttons.values():
            if enabled:
                if button.cget("fg_color") != BETTING_COLORS["locked"]:
                    button.configure(state="normal")
            else:
                button.configure(state="disabled")

        # Prop bet buttons
        for button in self.prop_bet_buttons.values():
            if enabled:
                if button.cget("fg_color") != BETTING_COLORS["locked"]:
                    button.configure(state="normal")
            else:
                button.configure(state="disabled")

        # Exotic finish buttons
        for button in self.exotic_finish_buttons.values():
            if enabled:
                if button.cget("fg_color") != BETTING_COLORS["locked"]:
                    button.configure(state="normal")
            else:
                button.configure(state="disabled")

    def reset_all_buttons(self):
        """Reset all buttons to original appearance."""
        # Reset standard betting buttons
        for horse in HORSES:
            horse_idx = HORSES.index(horse)
            horse_bets = BETTING_GRID[horse_idx]

            for bet_type in ["show", "place", "win"]:
                if bet_type in self.bet_buttons[horse]:
                    for btn_info in self.bet_buttons[horse][bet_type]:
                        self.reset_button_appearance(horse, bet_type, btn_info["row"], btn_info["col"])

        # Reset special bet buttons
        for bet_name in self.special_bet_buttons.keys():
            self.reset_special_bet_appearance(bet_name)

    def reset_button_appearance(self, horse: str, bet_type: str, row: int, col: int):
        """Reset button to original appearance."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]
                    penalty = btn_info["penalty"]

                    color = BETTING_COLORS[bet_type]
                    hover_color = BETTING_COLORS[f"hover_{bet_type}"]
                    text_color = BETTING_COLORS["text_dark"] if bet_type == "win" else BETTING_COLORS["text"]

                    if penalty > 0:
                        btn_text = f"{multiplier}x\n-${penalty}"
                    else:
                        btn_text = f"{multiplier}x\nFREE"

                    button.configure(
                        text=btn_text,
                        fg_color=color,
                        hover_color=hover_color,
                        text_color=text_color,
                        state="normal"
                    )
                    break

    def reset_special_bet_appearance(self, bet_name: str):
        """Reset special bet button to original appearance."""
        if bet_name in self.special_bet_buttons:
            button = self.special_bet_buttons[bet_name]

            # Find the original bet info
            color_map = {
                "blue": BETTING_COLORS["blue_bet"],
                "orange": BETTING_COLORS["orange_bet"],
                "red": BETTING_COLORS["red_bet"],
                "black": BETTING_COLORS["black_bet"]
            }

            for name, payout, color in SPECIAL_BETS:
                if name == bet_name:
                    if color in ["blue", "orange", "red"]:
                        btn_text = f"{name}\n🏆 {payout} | 💸 -$1"
                    else:
                        btn_text = f"{name}\n🏆 {payout} | ✅ FREE"

                    button.configure(
                        text=btn_text,
                        fg_color=color_map[color],
                        state="normal"  # MAKE SURE state is set to normal
                    )
                    break

    def reset_prop_buttons_to_purple(self, prop_bets: List[Dict]):
        """Reset prop bet buttons to original appearance."""
        for prop_bet in prop_bets:
            if prop_bet["id"] in self.prop_bet_buttons:
                self.reset_prop_bet_appearance(prop_bet["id"], prop_bet)

    def reset_prop_bet_appearance(self, prop_bet_id: int, prop_bet: Dict):
        """Reset prop bet button to original appearance."""
        if prop_bet_id in self.prop_bet_buttons:
            button = self.prop_bet_buttons[prop_bet_id]
            btn_text = f"{prop_bet['description']}\n💰 {prop_bet['multiplier']}x | 💸 -${prop_bet['penalty']}"

            button.configure(
                text=btn_text,
                fg_color=BETTING_COLORS["prop"],
                hover_color="#6d28d9",
                text_color="white",
                state="normal"
            )

    def reset_exotic_finishes_to_orange(self, exotic_finishes: List[Dict]):
        """Reset exotic finish buttons to original appearance."""
        for exotic_finish in exotic_finishes:
            if exotic_finish["id"] in self.exotic_finish_buttons:
                self.reset_exotic_finish_appearance(exotic_finish["id"], exotic_finish)

    def reset_exotic_finish_appearance(self, exotic_finish_id: int, exotic_finish: Dict):
        """Reset exotic finish button to original appearance."""
        if exotic_finish_id in self.exotic_finish_buttons:
            button = self.exotic_finish_buttons[exotic_finish_id]
            # CHANGE: Show FULL description without cutting it off
            btn_text = f"{exotic_finish['name']}\n{exotic_finish['description']}\n{exotic_finish['multiplier']}x | -${exotic_finish['penalty']}\nMax 3 players"

            button.configure(
                text=btn_text,
                fg_color=BETTING_COLORS["exotic"],
                hover_color="#0e7490",
                state="normal"
            )

    def clear_all_bets(self):
        """Clear all current bets."""
        if not self.game_state:
            return

        # Clear all bets from game state
        self.game_state.clear_all_bets()

        # Reset all button appearances
        self.reset_all_buttons()
        self.reset_prop_buttons_to_purple(
            self.game_state.current_prop_bets if self.game_state.current_prop_bets else [])
        self.reset_exotic_finishes_to_orange(
            self.game_state.current_exotic_finishes if self.game_state.current_exotic_finishes else [])

        # Update display
        self.update_bets_display({})

        # Update button states in main app if available
        if hasattr(self, 'main_app_callback'):
            self.main_app_callback()

    def _reset_bet_button(self, bet):
        """Reset a specific bet button to original appearance."""
        if bet.is_prop_bet():
            # Reset prop bet button
            if bet.prop_bet_id in self.prop_bet_buttons:
                prop_bet = next((p for p in self.game_state.current_prop_bets if p["id"] == bet.prop_bet_id), None)
                if prop_bet:
                    self.reset_prop_bet_appearance(bet.prop_bet_id, prop_bet)

        elif bet.is_exotic_bet():
            # Reset exotic finish button
            if bet.exotic_finish_id in self.exotic_finish_buttons:
                exotic_finish = next(
                    (ef for ef in self.game_state.current_exotic_finishes if ef["id"] == bet.exotic_finish_id), None)
                if exotic_finish:
                    # Get remaining players on this exotic finish
                    remaining_players = [b.player for b in self.game_state.current_bets.values()
                                         if
                                         b.is_exotic_bet() and b.exotic_finish_id == bet.exotic_finish_id and b.player != bet.player]
                    if remaining_players:
                        self.update_exotic_finish_appearance(bet.exotic_finish_id, remaining_players)
                    else:
                        self.reset_exotic_finish_appearance(bet.exotic_finish_id, exotic_finish)

        elif bet.is_special_bet():
            # Reset special bet button
            if bet.bet_type in self.special_bet_buttons:
                self.reset_special_bet_appearance(bet.bet_type)

        else:
            # Reset standard bet button
            if bet.row is not None and bet.col is not None:
                self.reset_button_appearance(bet.horse, bet.bet_type, bet.row, bet.col)

    def _create_bet_card(self, bet_id: str, bet):
        """Create an individual bet card with remove button."""
        # Bet card frame
        bet_card = ctk.CTkFrame(self.bets_scroll_frame, fg_color=BETTING_COLORS["card"])
        bet_card.pack(fill="x", padx=5, pady=3)
        bet_card.grid_columnconfigure(0, weight=1)

        # Bet info frame
        info_frame = ctk.CTkFrame(bet_card, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        info_frame.grid_columnconfigure(0, weight=1)

        # Format bet information
        penalty_text = f"-${bet.potential_loss}" if bet.potential_loss > 0 else "FREE"

        if bet.is_prop_bet():
            bet_info = f"🎯 PROP #{bet.prop_bet_id}"
            bet_color = BETTING_COLORS["prop"]
        elif bet.is_exotic_bet():
            bet_info = f"⭐ EXOTIC #{bet.exotic_finish_id}"
            bet_color = BETTING_COLORS["exotic"]
        elif bet.horse == "Special":
            bet_info = f"👑 {bet.bet_type}"
            bet_color = "#f59e0b"  # Orange for special bets
        else:
            bet_info = f"🐎 {bet.horse} {bet.bet_type.upper()}"
            bet_color = BETTING_COLORS[bet.bet_type] if bet.bet_type in BETTING_COLORS else "#3b82f6"

        # Player name and bet type
        player_label = ctk.CTkLabel(
            info_frame,
            text=f"🏇 {bet.player}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=bet_color
        )
        player_label.grid(row=0, column=0, sticky="w")

        # Bet details
        details_text = f"{bet_info} | 🎫 ${bet.token_value} | 💰 +${bet.potential_payout} | 💸 {penalty_text}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=ctk.CTkFont(size=11),
            text_color="#ffffff"
        )
        details_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Remove button
        remove_btn = ctk.CTkButton(
            bet_card,
            text="🗑️",
            font=ctk.CTkFont(size=14),
            fg_color="#ef4444",
            hover_color="#dc2626",
            width=40,
            height=30,
            command=lambda bid=bet_id: self.remove_specific_bet(bid)
        )
        remove_btn.grid(row=0, column=1, padx=(5, 10), pady=8)

    def remove_specific_bet(self, bet_id: str):
        """Remove a specific bet by ID."""
        if not self.game_state:
            return

        bet = self.game_state.current_bets.get(bet_id)
        if bet and self.game_state.remove_bet(bet_id):
            # Update the display
            self.update_bets_display(self.game_state.current_bets)
            # Reset button appearance
            self._reset_bet_button(bet)

            # Update button states in main app if available
            if hasattr(self, 'main_app_callback'):
                self.main_app_callback()

    def set_main_app_callback(self, callback):
        """Set callback to update main app when bets change."""
        self.main_app_callback = callback