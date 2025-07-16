"""Dialog windows for the Ready Set Bet application."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Callable


class BetDialog:
    """Base class for betting dialogs."""

    def __init__(self, parent, players: Dict, title: str = "Place Bet"):
        self.parent = parent
        self.players = players
        self.dialog = None
        self.result = None
        self.setup_dialog(title)

    def setup_dialog(self, title: str):
        """Set up the dialog window."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry("350x400")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

    def create_player_selection(self) -> tk.StringVar:
        """Create player selection combobox."""
        ttk.Label(self.dialog, text="Select Player:").pack(pady=5)
        player_var = tk.StringVar()
        player_combo = ttk.Combobox(self.dialog, textvariable=player_var, values=list(self.players.keys()))
        player_combo.pack(pady=5)
        return player_var


    def create_token_selection(self, player_var: tk.StringVar) -> tk.StringVar:
        """Create token selection interface."""
        token_frame = ttk.LabelFrame(self.dialog, text="Select Token Value", padding="10")
        token_frame.pack(pady=10, padx=20, fill="x")

        token_var = tk.StringVar()
        token_buttons = {}

        def update_token_display():
            player = player_var.get()
            if player and player in self.players:
                for value in ["5", "3", "2", "1"]:
                    available = self.players[player].get_available_tokens(value)
                    if available > 0:
                        token_buttons[value].configure(state="normal")
                        token_buttons[value].configure(text=f"${value} Token ({available} available)")
                    else:
                        token_buttons[value].configure(state="disabled", text=f"${value} Token (none left)")

        # Create token selection radio buttons
        for i, value in enumerate(["5", "3", "2", "1"]):
            btn = ttk.Radiobutton(token_frame, text=f"${value} Token",
                                  variable=token_var, value=value)
            btn.grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=2)
            token_buttons[value] = btn

        # Update tokens when player changes
        player_var.trace("w", lambda *args: update_token_display())

        return token_var


    def show(self) -> Optional[Dict]:
        """Show the dialog and return the result."""
        self.dialog.wait_window()
        return self.result


class StandardBetDialog(BetDialog):
    """Dialog for placing standard horse bets."""

    def __init__(self, parent, players: Dict, horse: str, bet_type: str, multiplier: int, penalty: int):
        self.horse = horse
        self.bet_type = bet_type
        self.multiplier = multiplier
        self.penalty = penalty
        super().__init__(parent, players, "Place Standard Bet")
        self.setup_content()

    def setup_content(self):
        """Set up the dialog content."""
        # Bet information
        ttk.Label(self.dialog, text=f"Horse {self.horse} - {self.bet_type.title()}",
                  font=("Arial", 12, "bold")).pack(pady=5)

        if self.penalty > 0:
            ttk.Label(self.dialog, text=f"Win: {self.multiplier}x multiplier | Lose: -${self.penalty} penalty",
                      font=("Arial", 10)).pack(pady=2)
        else:
            ttk.Label(self.dialog, text=f"Win: {self.multiplier}x multiplier | Lose: No penalty",
                      font=("Arial", 10), foreground="green").pack(pady=2)

        # Player and token selection
        player_var = self.create_player_selection()
        token_var = self.create_token_selection(player_var)

        # Calculation display
        calculation_label = ttk.Label(self.dialog, text="", font=("Arial", 11, "bold"))
        calculation_label.pack(pady=10)

        def update_calculation(*args):
            if token_var.get():
                token_value = int(token_var.get())
                potential_win = token_value * self.multiplier
                if self.penalty > 0:
                    calculation_label.configure(
                        text=f"If WIN: +${potential_win} | If LOSE: -${self.penalty}",
                        foreground="blue")
                else:
                    calculation_label.configure(
                        text=f"If WIN: +${potential_win} | If LOSE: No penalty",
                        foreground="green")
            else:
                calculation_label.configure(text="")

        token_var.trace("w", update_calculation)

        # Action button
        def place_bet_action():
            player = player_var.get()
            token_value = token_var.get()

            if not player:
                messagebox.showerror("Error", "Please select a player!")
                return

            if not token_value:
                messagebox.showerror("Error", "Please select a token!")
                return

            if self.players[player].get_available_tokens(token_value) <= 0:
                messagebox.showerror("Error", "No tokens of this value available!")
                return

            self.result = {
                "player": player,
                "token_value": int(token_value)
            }
            self.dialog.destroy()

        ttk.Button(self.dialog, text="Place Bet", command=place_bet_action).pack(pady=10)


class SpecialBetDialog(BetDialog):
    """Dialog for placing special bets."""

    def __init__(self, parent, players: Dict, bet_name: str, multiplier: int):
        self.bet_name = bet_name
        self.multiplier = multiplier
        super().__init__(parent, players, "Place Special Bet")
        self.setup_content()

    def setup_content(self):
        """Set up the dialog content."""
        # Bet information
        if self.bet_name == "7 Finishes 5th or Worse":
            ttk.Label(self.dialog, text=f"{self.bet_name} ({self.multiplier}x multiplier | No penalty)").pack(pady=5)
        else:
            ttk.Label(self.dialog, text=f"{self.bet_name} ({self.multiplier}x multiplier | -$1 penalty if lose)").pack(
                pady=5)

        # Player and token selection
        player_var = self.create_player_selection()
        token_var = self.create_token_selection(player_var)

        # Calculation display
        payout_label = ttk.Label(self.dialog, text="", font=("Arial", 12, "bold"), foreground="green")
        payout_label.pack(pady=10)

        def update_payout(*args):
            if token_var.get():
                token_value = int(token_var.get())
                potential_win = token_value * self.multiplier
                if self.bet_name == "7 Finishes 5th or Worse":
                    payout_label.configure(text=f"If WIN: +${potential_win} | If LOSE: No penalty", foreground="green")
                else:
                    payout_label.configure(text=f"If WIN: +${potential_win} | If LOSE: -$1")
            else:
                payout_label.configure(text="")

        token_var.trace("w", update_payout)

        # Action button
        def place_special_action():
            player = player_var.get()
            token_value = token_var.get()

            if not player:
                messagebox.showerror("Error", "Please select a player!")
                return

            if not token_value:
                messagebox.showerror("Error", "Please select a token!")
                return

            if self.players[player].get_available_tokens(token_value) <= 0:
                messagebox.showerror("Error", "No tokens of this value available!")
                return

            self.result = {
                "player": player,
                "token_value": int(token_value)
            }
            self.dialog.destroy()

        ttk.Button(self.dialog, text="Place Bet", command=place_special_action).pack(pady=10)


class PropBetDialog(BetDialog):
    """Dialog for placing prop bets."""

    def __init__(self, parent, players: Dict, prop_bet: Dict):
        self.prop_bet = prop_bet
        super().__init__(parent, players, "Place Prop Bet")
        self.setup_content()

    def setup_content(self):
        """Set up the dialog content."""
        # Bet information
        ttk.Label(self.dialog, text="Prop Bet", font=("Arial", 14, "bold")).pack(pady=5)
        ttk.Label(self.dialog, text=self.prop_bet["description"],
                  font=("Arial", 11, "bold"), wraplength=300).pack(pady=5)

        ttk.Label(self.dialog,
                  text=f"Win: {self.prop_bet['multiplier']}x multiplier | Lose: -${self.prop_bet['penalty']} penalty",
                  font=("Arial", 10)).pack(pady=2)

        # Player and token selection
        player_var = self.create_player_selection()
        token_var = self.create_token_selection(player_var)

        # Calculation display
        calculation_label = ttk.Label(self.dialog, text="", font=("Arial", 11, "bold"))
        calculation_label.pack(pady=10)

        def update_calculation(*args):
            if token_var.get():
                token_value = int(token_var.get())
                potential_win = token_value * self.prop_bet["multiplier"]
                calculation_label.configure(
                    text=f"If WIN: +${potential_win} | If LOSE: -${self.prop_bet['penalty']}",
                    foreground="purple")
            else:
                calculation_label.configure(text="")

        token_var.trace("w", update_calculation)

        # Action button
        def place_prop_action():
            player = player_var.get()
            token_value = token_var.get()

            if not player:
                messagebox.showerror("Error", "Please select a player!")
                return

            if not token_value:
                messagebox.showerror("Error", "Please select a token!")
                return

            if self.players[player].get_available_tokens(token_value) <= 0:
                messagebox.showerror("Error", "No tokens of this value available!")
                return

            self.result = {
                "player": player,
                "token_value": int(token_value),
                "prop_bet_id": self.prop_bet["id"]
            }
            self.dialog.destroy()

        ttk.Button(self.dialog, text="Place Prop Bet", command=place_prop_action).pack(pady=10)


class RaceResultsDialog:
    """Dialog for entering race results."""

    def __init__(self, parent, horses: List[str], prop_bets: List[Dict], current_bets: Dict):
        self.parent = parent
        self.horses = horses
        self.prop_bets = prop_bets
        self.current_bets = current_bets
        self.result = None
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the dialog."""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Enter Race Results")
        dialog.geometry("500x600")
        dialog.transient(self.parent)
        dialog.grab_set()

        # Create scrollable frame
        canvas = tk.Canvas(dialog)
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Horse results section
        ttk.Label(scrollable_frame, text="Enter finishing positions (separate multiple horses with commas):",
                  font=("Arial", 12, "bold")).pack(pady=10)

        entries = {}
        for i, position in enumerate(["Win (1st)", "Place (1st-2nd)", "Show (1st-3rd)"]):
            frame = ttk.Frame(scrollable_frame)
            frame.pack(pady=5)

            ttk.Label(frame, text=f"{position}:").pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, width=20)
            entry.pack(side=tk.LEFT, padx=5)
            entries[position] = entry

        # Examples
        ttk.Label(scrollable_frame, text="Examples:", font=("Arial", 9, "bold")).pack(pady=(10, 0))
        ttk.Label(scrollable_frame, text="Win: 7 (only one horse can win)", font=("Arial", 8)).pack()
        ttk.Label(scrollable_frame, text="Place: 7,2/3 (horses that finished 1st or 2nd)", font=("Arial", 8)).pack()
        ttk.Label(scrollable_frame, text="Show: 7,2/3,11/12 (horses that finished 1st, 2nd, or 3rd)", font=("Arial", 8)).pack()
        ttk.Label(scrollable_frame, text=f"Use horse names: {', '.join(self.horses)}", font=("Arial", 8)).pack()

        # Prop bet results section
        # Only show prop bets that have actual bets placed on them
        prop_bets_with_bets = self._get_prop_bets_with_bets()

        if prop_bets_with_bets:
            ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', pady=20)
            ttk.Label(scrollable_frame, text="Prop Bet Results:", font=("Arial", 12, "bold")).pack(pady=10)

            prop_vars = {}
            for prop_bet in prop_bets_with_bets:
                frame = ttk.Frame(scrollable_frame)
                frame.pack(pady=5, padx=20, fill='x')

                ttk.Label(frame, text=prop_bet["description"],
                         wraplength=300, font=("Arial", 9)).pack(anchor='w')

                var = tk.StringVar(value="")
                result_frame = ttk.Frame(frame)
                result_frame.pack(anchor='w', pady=2)

                ttk.Radiobutton(result_frame, text="Won", variable=var, value="won").pack(side=tk.LEFT, padx=5)
                ttk.Radiobutton(result_frame, text="Lost", variable=var, value="lost").pack(side=tk.LEFT, padx=5)

                prop_vars[prop_bet["id"]] = var

        def process_results():
            try:
                # Parse horses
                win_text = entries["Win (1st)"].get().strip()
                win_horses = [h.strip() for h in win_text.split(',') if h.strip()]

                place_text = entries["Place (1st-2nd)"].get().strip()
                place_horses = [h.strip() for h in place_text.split(',') if h.strip()]

                show_text = entries["Show (1st-3rd)"].get().strip()
                show_horses = [h.strip() for h in show_text.split(',') if h.strip()]

                # Validate
                all_horses = win_horses + place_horses + show_horses
                valid_horses = set(self.horses)
                if not all(h in valid_horses for h in all_horses):
                    messagebox.showerror("Error", f"All horses must be one of: {', '.join(self.horses)}")
                    return

                if not win_horses or not place_horses or not show_horses:
                    messagebox.showerror("Error", "All position types must have at least one horse!")
                    return

                # Parse prop bet results
                prop_results = {}
                prop_bets_with_bets = self._get_prop_bets_with_bets()
                if prop_bets_with_bets:
                    for prop_bet in prop_bets_with_bets:
                        prop_id = prop_bet["id"]
                        result = prop_vars[prop_id].get()
                        if result == "won":
                            prop_results[prop_id] = True
                        elif result == "lost":
                            prop_results[prop_id] = False
                        else:
                            messagebox.showerror("Error", f"Please select a result for prop bet: {prop_bet['description'][:30]}...")
                            return

                self.result = {
                    "win": win_horses,
                    "place": place_horses,
                    "show": show_horses,
                    "prop_results": prop_results
                }
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Please enter valid data: {str(e)}")

        ttk.Button(scrollable_frame, text="Process Results", command=process_results).pack(pady=20)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        dialog.wait_window()

    def _get_prop_bets_with_bets(self) -> List[Dict]:
        """Get only the prop bets that have actual bets placed on them."""
        prop_bets_with_bets = []

        # Find which prop bets have actual bets
        prop_bet_ids_with_bets = set()
        for bet in self.current_bets.values():
            if bet.is_prop_bet():
                prop_bet_ids_with_bets.add(bet.prop_bet_id)

        # Return only prop bets that have bets placed
        for prop_bet in self.prop_bets:
            if prop_bet["id"] in prop_bet_ids_with_bets:
                prop_bets_with_bets.append(prop_bet)

        return prop_bets_with_bets


class AddPlayerDialog:
    """Dialog for adding a new player."""

    def __init__(self, parent, existing_players: List[str]):
        self.parent = parent
        self.existing_players = existing_players
        self.result = None
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the dialog."""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add Player")
        dialog.geometry("300x150")
        dialog.transient(self.parent)
        dialog.grab_set()

        ttk.Label(dialog, text="Player Name:").pack(pady=10)
        name_entry = ttk.Entry(dialog, width=20)
        name_entry.pack(pady=5)
        name_entry.focus()

        def add_player_action():
            name = name_entry.get().strip()
            if name and name not in self.existing_players:
                self.result = name
                dialog.destroy()
            elif name in self.existing_players:
                messagebox.showerror("Error", "Player already exists!")
            else:
                messagebox.showerror("Error", "Please enter a valid name!")

        ttk.Button(dialog, text="Add Player", command=add_player_action).pack(pady=10)

        dialog.bind('<Return>', lambda e: add_player_action())
        dialog.wait_window()