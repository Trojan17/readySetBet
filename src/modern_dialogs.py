"""Modern dialog windows for the Ready Set Bet application using CustomTkinter."""

import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, List, Optional

from .constants import Theme, HORSES


class BaseDialog:
    """Base class for all dialog windows."""

    def __init__(self, parent, title: str, size: str = "450x500"):
        self.parent = parent
        self.dialog = None
        self.result = None
        self._setup_dialog(title, size)

    def _setup_dialog(self, title: str, size: str):
        """Set up the basic dialog window."""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry(size)
        self.dialog.configure(fg_color=Theme.SURFACE)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

    def center_on_parent(self):
        """Center dialog on parent window and auto-resize if needed."""
        self.dialog.update_idletasks()

        # Get required size
        req_width = self.dialog.winfo_reqwidth()
        req_height = self.dialog.winfo_reqheight()

        # Set minimum size and auto-expand if needed
        current_width = int(self.dialog.winfo_width())
        current_height = int(self.dialog.winfo_height())

        # Use larger of current size or required size, with some padding
        final_width = max(current_width, req_width + 50, 450)
        final_height = max(current_height, req_height + 50, 400)

        # Don't make it too large
        max_width = int(self.dialog.winfo_screenwidth() * 0.6)
        max_height = int(self.dialog.winfo_screenheight() * 0.8)

        final_width = min(final_width, max_width)
        final_height = min(final_height, max_height)

        # Center on parent
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        x = parent_x + (parent_width // 2) - (final_width // 2)
        y = parent_y + (parent_height // 2) - (final_height // 2)

        self.dialog.geometry(f"{final_width}x{final_height}+{x}+{y}")

    def show(self) -> Optional[dict]:
        """Show dialog and return result."""
        self.dialog.wait_window()
        return self.result

    def close(self):
        """Close the dialog."""
        self.dialog.destroy()


class BetDialog(BaseDialog):
    """Base dialog for all betting actions."""

    def __init__(self, parent, players: Dict, title: str, bet_info: dict):
        self.players = players
        self.bet_info = bet_info
        super().__init__(parent, title, "500x600")  # Increased size from 450x500 to 500x600
        self._setup_content()
        self.center_on_parent()

    def _setup_content(self):
        """Set up dialog content."""
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text=self.bet_info.get('title', 'Place Bet'),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.bet_info.get('color', Theme.ACCENT)
        )
        title_label.pack(pady=(20, 10))

        # Bet information
        info_frame = ctk.CTkFrame(self.dialog, fg_color=Theme.CARD)
        info_frame.pack(pady=10, padx=30, fill="x")

        info_text = self._format_bet_info()
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            text_color=self.bet_info.get('color', Theme.ACCENT)
        ).pack(pady=15)

        # Player selection
        player_frame = ctk.CTkFrame(self.dialog, fg_color=Theme.CARD)
        player_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(
            player_frame,
            text="Select Player",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))

        self.player_var = ctk.StringVar()
        self.player_combo = ctk.CTkComboBox(
            player_frame,
            variable=self.player_var,
            values=list(self.players.keys()),  # Changed from players.keys() to self.players.keys()
            state="readonly",
            width=250
        )
        self.player_combo.pack(pady=(0, 15))

        # Token selection
        token_frame = ctk.CTkFrame(self.dialog, fg_color=Theme.CARD)
        token_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(
            token_frame,
            text="Select Token Value",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))

        self.token_var = ctk.StringVar()
        self.token_buttons = {}

        radio_frame = ctk.CTkFrame(token_frame, fg_color="transparent")
        radio_frame.pack(pady=(0, 15))

        for i, value in enumerate(["5", "3", "2", "1"]):
            btn = ctk.CTkRadioButton(
                radio_frame,
                text=f"${value} Token",
                variable=self.token_var,
                value=value,
                font=ctk.CTkFont(size=11)
            )
            btn.grid(row=i//2, column=i%2, pady=5, padx=20, sticky="w")
            self.token_buttons[value] = btn

        # Set up event handlers
        self.player_var.trace("w", lambda *args: self.update_token_display())

        # Calculation display
        calc_frame = ctk.CTkFrame(self.dialog, fg_color=Theme.SURFACE)
        calc_frame.pack(pady=10, padx=30, fill="x")

        self.calculation_label = ctk.CTkLabel(
            calc_frame,
            text="Select a token to see potential payout",
            font=ctk.CTkFont(size=12),
            text_color=Theme.ACCENT
        )
        self.calculation_label.pack(pady=10)

        self.token_var.trace("w", lambda *args: self.update_calculation())

        # Action buttons
        self._setup_buttons()

    def _format_bet_info(self) -> str:
        """Format bet information for display."""
        multiplier = self.bet_info.get('multiplier', 1)
        penalty = self.bet_info.get('penalty', 0)
        description = self.bet_info.get('description', '')

        info_parts = []
        if description:
            info_parts.append(description)

        if penalty > 0:
            info_parts.append(f"🏆 Win: {multiplier}x multiplier\n💸 Lose: -${penalty} penalty")
        else:
            info_parts.append(f"🏆 Win: {multiplier}x multiplier\n✅ Lose: No penalty")

        return "\n\n".join(info_parts)

    def _setup_buttons(self):
        """Set up action buttons."""
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=30, fill="x")

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.close,
            fg_color=Theme.DISABLED,
            font=ctk.CTkFont(size=14)
        )
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        place_btn = ctk.CTkButton(
            button_frame,
            text="🎲 Place Bet",
            command=self._place_bet,
            fg_color=Theme.SUCCESS,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        place_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def update_token_display(self):
        """Update token button states based on selected player."""
        player_name = self.player_var.get()
        if player_name and player_name in self.players:
            player = self.players[player_name]
            for value in ["5", "3", "2", "1"]:
                available = player.get_available_tokens(value)
                btn = self.token_buttons[value]
                if available > 0:
                    btn.configure(
                        state="normal",
                        text=f"${value} Token ({available} available)"
                    )
                else:
                    btn.configure(
                        state="disabled",
                        text=f"${value} Token (none left)"
                    )

    def update_calculation(self):
        """Update the payout calculation display."""
        if not self.token_var.get():
            self.calculation_label.configure(
                text="Select a token to see potential payout",
                text_color=Theme.ACCENT
            )
            return

        token_value = int(self.token_var.get())
        multiplier = self.bet_info.get('multiplier', 1)
        penalty = self.bet_info.get('penalty', 0)

        potential_win = token_value * multiplier

        if penalty > 0:
            calc_text = f"💰 If WIN: +${potential_win} | 💸 If LOSE: -${penalty}"
            text_color = Theme.WARNING
        else:
            calc_text = f"💰 If WIN: +${potential_win} | ✅ If LOSE: No penalty"
            text_color = Theme.SUCCESS

        self.calculation_label.configure(text=calc_text, text_color=text_color)

    def _place_bet(self):
        """Handle bet placement."""
        player = self.player_var.get()
        token_value = self.token_var.get()

        if not player:
            messagebox.showerror("Error", "Please select a player!")
            return
        if not token_value:
            messagebox.showerror("Error", "Please select a token!")
            return

        if self.players[player].get_available_tokens(token_value) <= 0:
            messagebox.showerror("Error", "No tokens of this value available!")
            return

        self.result = {"player": player, "token_value": int(token_value)}
        self.close()


class ModernStandardBetDialog(BetDialog):
    """Dialog for standard horse betting."""

    def __init__(self, parent, players: Dict, horse: str, bet_type: str,
                 multiplier: int, penalty: int):
        bet_info = {
            'title': f"🐎 Horse {horse} - {bet_type.title()}",
            'color': Theme.WIN,
            'multiplier': multiplier,
            'penalty': penalty
        }
        super().__init__(parent, players, "Place Standard Bet", bet_info)


class ModernSpecialBetDialog(BetDialog):
    """Dialog for special betting."""

    def __init__(self, parent, players: Dict, bet_name: str, multiplier: int):
        penalty = 0 if bet_name == "7 Finishes 5th or Worse" else 1

        bet_info = {
            'title': f"👑 {bet_name}",
            'color': Theme.WARNING,
            'multiplier': multiplier,
            'penalty': penalty
        }
        super().__init__(parent, players, "Place Special Bet", bet_info)


class ModernPropBetDialog(BetDialog):
    """Dialog for proposition betting."""

    def __init__(self, parent, players: Dict, prop_bet: Dict):
        bet_info = {
            'title': "🎯 Proposition Bet",
            'color': Theme.PROP,
            'description': prop_bet["description"],
            'multiplier': prop_bet["multiplier"],
            'penalty': prop_bet["penalty"]
        }
        # Override parent init to use larger size for prop bets
        self.players = players
        self.bet_info = bet_info
        BaseDialog.__init__(self, parent, "Place Prop Bet", "550x650")  # Even larger for prop bets
        self._setup_content()
        self.center_on_parent()


class ModernExoticFinishDialog(BetDialog):
    """Dialog for exotic finish betting."""

    def __init__(self, parent, players: Dict, exotic_finish: Dict):
        bet_info = {
            'title': f"⭐ {exotic_finish['name']}",
            'color': Theme.EXOTIC,
            'description': exotic_finish["description"],
            'multiplier': exotic_finish["multiplier"],
            'penalty': exotic_finish["penalty"]
        }
        # Override parent init to use larger size for exotic finishes
        self.players = players
        self.bet_info = bet_info
        BaseDialog.__init__(self, parent, "Place Exotic Finish Bet", "550x650")  # Even larger for exotic finishes
        self._setup_content()
        self.center_on_parent()


class ModernAddPlayerDialog(BaseDialog):
    """Dialog for adding players."""

    def __init__(self, parent, existing_players: List[str]):
        self.existing_players = existing_players
        super().__init__(parent, "Add New Player", "400x200")
        self._setup_content()
        self.center_on_parent()

    def _setup_content(self):
        """Set up dialog content."""
        ctk.CTkLabel(
            self.dialog,
            text="👤 Add New Player",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=20)

        ctk.CTkLabel(
            self.dialog,
            text="Player Name:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 5))

        self.name_entry = ctk.CTkEntry(
            self.dialog,
            font=ctk.CTkFont(size=14),
            width=300,
            height=35
        )
        self.name_entry.pack(pady=(0, 20))
        self.name_entry.focus()

        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.close,
            fg_color=Theme.DISABLED,
            font=ctk.CTkFont(size=14),
            width=120
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="➕ Add Player",
            command=self._add_player,
            fg_color=Theme.SUCCESS,
            font=ctk.CTkFont(size=14),
            width=120
        ).pack(side="right", padx=10)

        # Enter key binding
        self.dialog.bind('<Return>', lambda e: self._add_player())

    def _add_player(self):
        """Handle adding a player."""
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter a valid name!")
            return

        if name in self.existing_players:
            messagebox.showerror("Error", "Player already exists!")
            return

        self.result = name
        self.close()


class ModernRaceResultsDialog(BaseDialog):
    """Dialog for entering race results."""

    def __init__(self, parent, horses: List[str], prop_bets: List[Dict],
                 exotic_finishes: List[Dict], current_bets: Dict):
        self.horses = horses
        self.prop_bets = self._filter_bets_with_players(prop_bets, current_bets, 'prop')
        self.exotic_finishes = self._filter_bets_with_players(exotic_finishes, current_bets, 'exotic')
        super().__init__(parent, "🏁 Enter Race Results", "600x700")
        self._setup_content()
        self.center_on_parent()

    def _filter_bets_with_players(self, bets: List[Dict], current_bets: Dict, bet_type: str) -> List[Dict]:
        """Filter to only bets that have players betting on them."""
        bet_ids_with_players = set()

        for bet in current_bets.values():
            if bet_type == 'prop' and bet.is_prop_bet():
                bet_ids_with_players.add(bet.prop_bet_id)
            elif bet_type == 'exotic' and bet.is_exotic_bet():
                bet_ids_with_players.add(bet.exotic_finish_id)

        return [bet for bet in bets if bet["id"] in bet_ids_with_players]

    def _setup_content(self):
        """Set up dialog content."""
        main_frame = ctk.CTkScrollableFrame(self.dialog, fg_color=Theme.SURFACE)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(
            main_frame,
            text="🏁 Enter Race Results",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=Theme.WIN
        ).pack(pady=(0, 20))

        # Horse results
        self._setup_horse_results(main_frame)

        # Prop bet results
        if self.prop_bets:
            self._setup_prop_results(main_frame)

        # Exotic finish results
        if self.exotic_finishes:
            self._setup_exotic_results(main_frame)

        # Action buttons
        self._setup_action_buttons(main_frame)

    def _setup_horse_results(self, parent):
        """Set up horse finishing positions section."""
        horse_frame = ctk.CTkFrame(parent, fg_color=Theme.CARD)
        horse_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            horse_frame,
            text="🐎 Horse Finishing Positions",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))

        ctk.CTkLabel(
            horse_frame,
            text="Enter horses separated by commas (e.g., 7,2/3,11/12)",
            font=ctk.CTkFont(size=12),
            text_color=Theme.ACCENT
        ).pack(pady=(0, 15))

        self.entries = {}
        positions = ["Win (1st)", "Place (1st-2nd)", "Show (1st-3rd)"]

        for position in positions:
            entry_frame = ctk.CTkFrame(horse_frame, fg_color="transparent")
            entry_frame.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                entry_frame,
                text=f"{position}:",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=120
            ).pack(side="left", padx=(0, 10))

            entry = ctk.CTkEntry(
                entry_frame,
                font=ctk.CTkFont(size=12),
                placeholder_text=f"Enter {position.lower()} horses..."
            )
            entry.pack(side="left", fill="x", expand=True)
            self.entries[position] = entry

        ctk.CTkLabel(
            horse_frame,
            text=f"Available horses: {', '.join(self.horses)}",
            font=ctk.CTkFont(size=10),
            text_color=Theme.ACCENT
        ).pack(pady=(10, 15))

    def _setup_prop_results(self, parent):
        """Set up proposition bet results section."""
        prop_frame = ctk.CTkFrame(parent, fg_color=Theme.CARD)
        prop_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            prop_frame,
            text="🎯 Proposition Bet Results",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Theme.PROP
        ).pack(pady=(15, 10))

        self.prop_vars = {}

        for prop_bet in self.prop_bets:
            bet_frame = ctk.CTkFrame(prop_frame, fg_color=Theme.SURFACE)
            bet_frame.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                bet_frame,
                text=prop_bet["description"],
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(anchor="w", padx=15, pady=(10, 5))

            var = ctk.StringVar()
            result_frame = ctk.CTkFrame(bet_frame, fg_color="transparent")
            result_frame.pack(anchor="w", padx=15, pady=(0, 10))

            ctk.CTkRadioButton(
                result_frame,
                text="✅ Won",
                variable=var,
                value="won",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(0, 20))

            ctk.CTkRadioButton(
                result_frame,
                text="❌ Lost",
                variable=var,
                value="lost",
                font=ctk.CTkFont(size=11)
            ).pack(side="left")

            self.prop_vars[prop_bet["id"]] = var

    def _setup_exotic_results(self, parent):
        """Set up exotic finish results section."""
        exotic_frame = ctk.CTkFrame(parent, fg_color=Theme.CARD)
        exotic_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            exotic_frame,
            text="⭐ Exotic Finish Results",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Theme.EXOTIC
        ).pack(pady=(15, 10))

        self.exotic_vars = {}

        for exotic_finish in self.exotic_finishes:
            bet_frame = ctk.CTkFrame(exotic_frame, fg_color=Theme.SURFACE)
            bet_frame.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(
                bet_frame,
                text=exotic_finish["name"],
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=Theme.EXOTIC
            ).pack(anchor="w", padx=15, pady=(10, 5))

            ctk.CTkLabel(
                bet_frame,
                text=exotic_finish["description"],
                font=ctk.CTkFont(size=11),
                wraplength=400
            ).pack(anchor="w", padx=15, pady=(0, 5))

            var = ctk.StringVar()
            result_frame = ctk.CTkFrame(bet_frame, fg_color="transparent")
            result_frame.pack(anchor="w", padx=15, pady=(0, 10))

            ctk.CTkRadioButton(
                result_frame,
                text="✅ Won",
                variable=var,
                value="won",
                font=ctk.CTkFont(size=11)
            ).pack(side="left", padx=(0, 20))

            ctk.CTkRadioButton(
                result_frame,
                text="❌ Lost",
                variable=var,
                value="lost",
                font=ctk.CTkFont(size=11)
            ).pack(side="left")

            self.exotic_vars[exotic_finish["id"]] = var

    def _setup_action_buttons(self, parent):
        """Set up action buttons."""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.close,
            fg_color=Theme.DISABLED,
            font=ctk.CTkFont(size=14),
            height=40
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            button_frame,
            text="🏁 Process Results",
            command=self._process_results,
            fg_color=Theme.SUCCESS,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        ).pack(side="right", fill="x", expand=True, padx=(10, 0))

    def _process_results(self):
        """Process and validate the race results."""
        try:
            # Parse horse results
            horse_results = {}
            for position, entry in self.entries.items():
                horses_text = entry.get().strip()
                horses = [h.strip() for h in horses_text.split(',') if h.strip()]

                if not horses:
                    messagebox.showerror("Error", f"Please enter horses for {position}!")
                    return

                # Validate horses
                for horse in horses:
                    if horse not in self.horses:
                        messagebox.showerror("Error", f"Invalid horse: {horse}")
                        return

                horse_results[position] = horses

            # Parse prop bet results
            prop_results = {}
            for prop_bet in self.prop_bets:
                prop_id = prop_bet["id"]
                result = self.prop_vars[prop_id].get()

                if not result:
                    messagebox.showerror("Error", f"Please select result for prop bet: {prop_bet['description'][:30]}...")
                    return

                prop_results[prop_id] = (result == "won")

            # Parse exotic finish results
            exotic_results = {}
            for exotic_finish in self.exotic_finishes:
                exotic_id = exotic_finish["id"]
                result = self.exotic_vars[exotic_id].get()

                if not result:
                    messagebox.showerror("Error", f"Please select result for: {exotic_finish['name']}")
                    return

                exotic_results[exotic_id] = (result == "won")

            # Prepare final result
            self.result = {
                "win": horse_results["Win (1st)"],
                "place": horse_results["Place (1st-2nd)"],
                "show": horse_results["Show (1st-3rd)"],
                "prop_results": prop_results,
                "exotic_results": exotic_results
            }

            print(f"DEBUG: Race results processed: {self.result}")  # Debug print
            self.close()

        except Exception as e:
            print(f"DEBUG: Error processing results: {e}")  # Debug print
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Please enter valid data: {str(e)}")