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


class RaceResultsDialog:
    """Dialog for entering race results."""

    def __init__(self, parent, horses: List[str]):
        self.parent = parent
        self.horses = horses
        self.result = None
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the dialog."""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Enter Race Results")
        dialog.geometry("400x300")
        dialog.transient(self.parent)
        dialog.grab_set()

        ttk.Label(dialog, text="Enter finishing positions (separate multiple horses with commas):").pack(pady=10)

        entries = {}
        for i, position in enumerate(["Win (1st)", "Place (1st-2nd)", "Show (1st-3rd)"]):
            frame = ttk.Frame(dialog)
            frame.pack(pady=5)

            ttk.Label(frame, text=f"{position}:").pack(side=tk.LEFT, padx=5)
            entry = ttk.Entry(frame, width=20)
            entry.pack(side=tk.LEFT, padx=5)
            entries[position] = entry

        # Examples
        ttk.Label(dialog, text="Examples:", font=("Arial", 9, "bold")).pack(pady=(10, 0))
        ttk.Label(dialog, text="Win: 7 (only one horse can win)", font=("Arial", 8)).pack()
        ttk.Label(dialog, text="Place: 7,2/3 (horses that finished 1st or 2nd)", font=("Arial", 8)).pack()
        ttk.Label(dialog, text="Show: 7,2/3,11/12 (horses that finished 1st, 2nd, or 3rd)", font=("Arial", 8)).pack()
        ttk.Label(dialog, text=f"Use horse names: {', '.join(self.horses)}", font=("Arial", 8)).pack()

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

                self.result = {
                    "win": win_horses,
                    "place": place_horses,
                    "show": show_horses
                }
                dialog.destroy()

            except Exception as e:
                messagebox.showerror("Error", f"Please enter valid horse names: {str(e)}")

        ttk.Button(dialog, text="Process Results", command=process_results).pack(pady=20)
        dialog.wait_window()


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
