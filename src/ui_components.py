"""UI components and widgets for the Ready Set Bet application."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional
from .constants import COLORS, SPECIAL_BETS, HORSES, HORSE_COLORS, BETTING_GRID


class BettingBoard:
    """Handles the betting board UI component."""

    def __init__(self, parent, on_standard_bet: Callable, on_special_bet: Callable, on_prop_bet: Callable):
        self.parent = parent
        self.on_standard_bet = on_standard_bet
        self.on_special_bet = on_special_bet
        self.on_prop_bet = on_prop_bet
        self.bet_buttons = {}
        self.prop_bet_buttons = {}
        self.special_bet_buttons = {}
        self.setup_board()

    def setup_board(self):
        """Set up the betting board UI."""
        # Main betting board frame
        board_frame = ttk.Frame(self.parent)
        board_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Prop bets (at the top)
        self._setup_prop_bets(board_frame)

        # Special bets
        self._setup_special_bets(board_frame)

        # Main betting grid
        self._setup_main_grid(board_frame)

        # Current bets display
        self._setup_current_bets(board_frame)

    def _setup_prop_bets(self, parent):
        """Set up the prop bets section."""
        self.prop_frame = ttk.LabelFrame(parent, text="Prop Bets", padding="5")
        self.prop_frame.grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        # Will be populated by update_prop_bets method

    def update_prop_bets(self, prop_bets: List[Dict]):
        """Update the prop bets display."""
        # Clear existing prop bet buttons
        for widget in self.prop_frame.winfo_children():
            widget.destroy()
        self.prop_bet_buttons.clear()

        if not prop_bets:
            ttk.Label(self.prop_frame, text="No prop bets for this race").pack(pady=10)
            return

        # Create prop bet buttons
        for i, prop_bet in enumerate(prop_bets):
            btn_text = f"{prop_bet['description']}\n{prop_bet['multiplier']}x\n(-${prop_bet['penalty']})"

            btn = tk.Button(self.prop_frame, text=btn_text, font=("Arial", 8, "bold"),
                            bg=COLORS["prop"]["bg"], fg=COLORS["prop"]["fg"],
                            activebackground=COLORS["prop"]["bg"], activeforeground=COLORS["prop"]["fg"],
                            relief="raised", bd=2, wraplength=120, height=4,
                            command=lambda pb=prop_bet: self.on_prop_bet(pb))
            btn.grid(row=0, column=i, padx=2, sticky="ew")
            self.prop_frame.columnconfigure(i, weight=1)
            self.prop_bet_buttons[prop_bet["id"]] = btn

    def _setup_special_bets(self, parent):
        """Set up the special bets section."""
        special_frame = ttk.Frame(parent)
        special_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="ew")

        for i, (name, payout, color) in enumerate(SPECIAL_BETS):
            color_config = COLORS["special"][color]

            # Only color bets have penalty, not the "7 Finishes 5th or Worse"
            if color in ["blue", "orange", "red"]:
                btn_text = f"{name}\n{payout}\n(-$1)"
            else:
                btn_text = f"{name}\n{payout}"

            btn = tk.Button(special_frame, text=btn_text, font=("Arial", 9, "bold"),
                            bg=color_config["bg"], fg=color_config["fg"],
                            activebackground=color_config["bg"], activeforeground=color_config["fg"],
                            relief="raised", bd=2,
                            command=lambda n=name, p=int(payout[:-1]): self.on_special_bet(n, p))
            btn.grid(row=0, column=i, padx=2, sticky="ew")
            special_frame.columnconfigure(i, weight=1)
            self.special_bet_buttons[name] = btn

    def _setup_main_grid(self, parent):
        """Set up the main betting grid."""
        main_frame = ttk.Frame(parent)
        main_frame.grid(row=2, column=0, sticky="nsew")

        # Headers
        self._setup_headers(main_frame)

        # Betting buttons
        self._setup_betting_buttons(main_frame)

        # Configure grid weights
        for i in range(8):
            main_frame.columnconfigure(i, weight=1)

    def _setup_headers(self, parent):
        """Set up the column headers."""
        headers = [
            ("SHOW", COLORS["show"], 0, 2),
            ("PLACE", COLORS["place"], 2, 2),
            ("WIN", COLORS["win"], 4, 3)
        ]

        for text, color_config, col, span in headers:
            header = tk.Label(parent, text=text, font=("Arial", 14, "bold"),
                              bg=color_config["bg"], fg=color_config["fg"],
                              relief="raised", bd=2)
            header.grid(row=0, column=col, columnspan=span, sticky="ew", padx=1, pady=1)

    def _setup_betting_buttons(self, parent):
        """Set up the betting buttons."""
        for horse_idx, horse in enumerate(HORSES):
            row = horse_idx + 1

            # Horse label
            horse_label = tk.Label(parent, text=horse, font=("Arial", 10, "bold"),
                                   bg=HORSE_COLORS.get(horse, "gray"), fg="white")
            horse_label.grid(row=row, column=7, padx=2, pady=1, sticky="ew")

            # Betting spots
            horse_bets = BETTING_GRID[horse_idx]
            self.bet_buttons[horse] = {}

            for col_idx, (multiplier, penalty) in enumerate(horse_bets):
                bet_type = "show" if col_idx < 2 else "place" if col_idx < 4 else "win"
                color_config = COLORS[bet_type]

                btn_text = f"{multiplier}x\n(-${penalty})" if penalty > 0 else f"{multiplier}x\n "

                btn = tk.Button(parent, text=btn_text, font=("Arial", 8, "bold"),
                                bg=color_config["bg"], fg=color_config["fg"],
                                activebackground=color_config["bg"], activeforeground=color_config["fg"],
                                relief="raised", bd=2,
                                command=lambda h=horse, t=bet_type, m=multiplier, p=penalty, r=row, c=col_idx:
                                self.on_standard_bet(h, t, m, p, r, c))
                btn.grid(row=row, column=col_idx, padx=1, pady=1, sticky="ew")

                if bet_type not in self.bet_buttons[horse]:
                    self.bet_buttons[horse][bet_type] = []
                self.bet_buttons[horse][bet_type].append({
                    "button": btn,
                    "row": row,
                    "col": col_idx,
                    "multiplier": multiplier,
                    "penalty": penalty
                })

    def _setup_current_bets(self, parent):
        """Set up the current bets display."""
        bets_frame = ttk.LabelFrame(parent, text="Current Bets", padding="5")
        bets_frame.grid(row=3, column=0, pady=(10, 0), sticky="ew")

        # Treeview for bets
        self.bets_tree = ttk.Treeview(bets_frame,
                                      columns=("Player", "Horse", "Type", "Token", "Win", "Lose", "Remove"),
                                      show="headings", height=6)

        # Configure columns
        columns = [
            ("Player", 60), ("Horse", 45), ("Type", 65), ("Token", 45),
            ("Win", 50), ("Lose", 50), ("Remove", 55)
        ]

        for col, width in columns:
            self.bets_tree.heading(col, text=col)
            self.bets_tree.column(col, width=width)

        # Scrollbar
        bets_scrollbar = ttk.Scrollbar(bets_frame, orient=tk.VERTICAL, command=self.bets_tree.yview)
        self.bets_tree.configure(yscrollcommand=bets_scrollbar.set)

        self.bets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Buttons
        button_frame = ttk.Frame(bets_frame)
        button_frame.pack(pady=(5, 0), fill="x")

        self.remove_btn = ttk.Button(button_frame, text="Remove Selected Bet")
        self.remove_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_btn = ttk.Button(button_frame, text="Clear All Bets")
        self.clear_btn.pack(side=tk.LEFT)

    def update_button_appearance(self, horse: str, bet_type: str, row: int, col: int, player: str):
        """Update button appearance to show it's locked."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]

                    new_text = f"{multiplier}x\n{player[:6]}"
                    button.configure(
                        text=new_text,
                        bg=COLORS["locked"]["bg"],
                        fg=COLORS["locked"]["fg"],
                        activebackground=COLORS["locked"]["bg"],
                        activeforeground=COLORS["locked"]["fg"],
                        state="disabled"
                    )
                    break

    def update_special_bet_appearance(self, bet_name: str, player: str):
        """Update special bet button appearance to show it's locked."""
        if bet_name in self.special_bet_buttons:
            button = self.special_bet_buttons[bet_name]
            current_text = button.cget("text")
            lines = current_text.split('\n')
            if len(lines) >= 2:
                new_text = f"{lines[0]}\n{lines[1]}\n{player[:8]}"
            else:
                new_text = f"{current_text}\n{player[:8]}"

            button.configure(
                text=new_text,
                bg=COLORS["locked"]["bg"],
                fg=COLORS["locked"]["fg"],
                activebackground=COLORS["locked"]["bg"],
                activeforeground=COLORS["locked"]["fg"],
                state="disabled"
            )

    def update_prop_bet_appearance(self, prop_bet_id: int, player: str):
        """Update prop bet button appearance to show it's locked."""
        if prop_bet_id in self.prop_bet_buttons:
            button = self.prop_bet_buttons[prop_bet_id]
            current_text = button.cget("text")
            lines = current_text.split('\n')
            if len(lines) >= 3:
                new_text = f"{lines[0]}\n{lines[1]}\n{player[:8]}"
            else:
                new_text = f"{current_text}\n{player[:8]}"

            button.configure(
                text=new_text,
                bg=COLORS["locked"]["bg"],
                fg=COLORS["locked"]["fg"],
                activebackground=COLORS["locked"]["bg"],
                activeforeground=COLORS["locked"]["fg"],
                state="disabled"
            )

    def reset_button_appearance(self, horse: str, bet_type: str, row: int, col: int):
        """Reset button to original appearance."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]
                    penalty = btn_info["penalty"]

                    color_config = COLORS[bet_type]
                    btn_text = f"{multiplier}x\n(-${penalty})" if penalty > 0 else f"{multiplier}x\n "

                    button.configure(
                        text=btn_text,
                        bg=color_config["bg"],
                        fg=color_config["fg"],
                        activebackground=color_config["bg"],
                        activeforeground=color_config["fg"],
                        state="normal"
                    )
                    break

    def reset_special_bet_appearance(self, bet_name: str):
        """Reset special bet button to original appearance."""
        if bet_name in self.special_bet_buttons:
            button = self.special_bet_buttons[bet_name]

            # Find the original bet info
            for name, payout, color in SPECIAL_BETS:
                if name == bet_name:
                    color_config = COLORS["special"][color]

                    if color in ["blue", "orange", "red"]:
                        btn_text = f"{name}\n{payout}\n(-$1)"
                    else:
                        btn_text = f"{name}\n{payout}"

                    button.configure(
                        text=btn_text,
                        bg=color_config["bg"],
                        fg=color_config["fg"],
                        activebackground=color_config["bg"],
                        activeforeground=color_config["fg"],
                        state="normal"
                    )
                    break

    def reset_prop_bet_appearance(self, prop_bet_id: int, prop_bet: Dict):
        """Reset prop bet button to original appearance."""
        if prop_bet_id in self.prop_bet_buttons:
            button = self.prop_bet_buttons[prop_bet_id]
            btn_text = f"{prop_bet['description']}\n{prop_bet['multiplier']}x\n(-${prop_bet['penalty']})"

            button.configure(
                text=btn_text,
                bg=COLORS["prop"]["bg"],
                fg=COLORS["prop"]["fg"],
                activebackground=COLORS["prop"]["bg"],
                activeforeground=COLORS["prop"]["fg"],
                state="normal"
            )

    def set_betting_enabled(self, enabled: bool):
        """Enable or disable all betting buttons."""
        # Standard betting buttons
        for horse in self.bet_buttons:
            for bet_type in self.bet_buttons[horse]:
                for btn_info in self.bet_buttons[horse][bet_type]:
                    button = btn_info["button"]
                    if enabled:
                        # Only enable if not already locked
                        if button.cget("bg") != COLORS["locked"]["bg"]:
                            button.configure(state="normal")
                    else:
                        button.configure(state="disabled")

        # Special bet buttons
        for button in self.special_bet_buttons.values():
            if enabled:
                # Only enable if not already locked
                if button.cget("bg") != COLORS["locked"]["bg"]:
                    button.configure(state="normal")
            else:
                button.configure(state="disabled")

        # Prop bet buttons
        for button in self.prop_bet_buttons.values():
            if enabled:
                # Only enable if not already locked
                if button.cget("bg") != COLORS["locked"]["bg"]:
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

    def reset_prop_buttons_to_purple(self, prop_bets: List[Dict]):
        """Reset prop bet buttons to their original purple appearance with full data."""
        for prop_bet in prop_bets:
            if prop_bet["id"] in self.prop_bet_buttons:
                self.reset_prop_bet_appearance(prop_bet["id"], prop_bet)

    def update_bets_display(self, bets: Dict):
        """Update the bets display."""
        # Clear existing items
        for item in self.bets_tree.get_children():
            self.bets_tree.delete(item)

        # Add current bets
        for bet in bets.values():
            penalty_text = f"-${bet.potential_loss}" if bet.potential_loss > 0 else "No penalty"

            # Determine bet type display
            if bet.is_prop_bet():
                horse_display = "Prop"
                type_display = f"Prop #{bet.prop_bet_id}"
            else:
                horse_display = bet.horse if bet.horse != "Special" else "Special"
                type_display = bet.bet_type

            self.bets_tree.insert("", tk.END, values=(
                bet.player,
                horse_display,
                type_display,
                f"${bet.token_value}",
                f"+${bet.potential_payout}",
                penalty_text,
                "🗑️"
            ))