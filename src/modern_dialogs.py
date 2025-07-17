"""Modern dialog windows for the Ready Set Bet application using CustomTkinter."""

import customtkinter as ctk
from tkinter import messagebox
from typing import Dict, List, Optional

# Modern color scheme
RACING_COLORS = {
    "primary": "#1f2937",
    "secondary": "#374151",
    "accent": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "surface": "#111827",
    "card": "#1f2937",
    "win": "#ffd700",
    "prop": "#8b5cf6",
    "exotic": "#f59e0b",
    "locked": "#6b7280"
}


class ModernBetDialog:
    """Base class for modern betting dialogs."""

    def __init__(self, parent, players: Dict, title: str = "Place Bet"):
        self.parent = parent
        self.players = players
        self.dialog = None
        self.result = None
        self.setup_dialog(title)

    def setup_dialog(self, title: str):
        """Set up the modern dialog window."""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title(title)
        self.dialog.geometry("450x500")
        self.dialog.minsize(400, 450)
        self.dialog.configure(fg_color=RACING_COLORS["surface"])
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

    def auto_resize_and_center(self):
        """Automatically resize dialog and center it."""
        self.dialog.update_idletasks()
        req_width = max(450, self.dialog.winfo_reqwidth() + 50)
        req_height = max(400, self.dialog.winfo_reqheight() + 50)
        max_width = int(self.dialog.winfo_screenwidth() * 0.6)
        max_height = int(self.dialog.winfo_screenheight() * 0.7)
        width = min(req_width, max_width)
        height = min(req_height, max_height)

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")

    def show(self) -> Optional[Dict]:
        """Show the dialog and return result."""
        self.dialog.wait_window()
        return self.result


class ModernStandardBetDialog(ModernBetDialog):
    """Modern dialog for placing standard horse bets."""

    def __init__(self, parent, players: Dict, horse: str, bet_type: str, multiplier: int, penalty: int):
        self.horse = horse
        self.bet_type = bet_type
        self.multiplier = multiplier
        self.penalty = penalty
        super().__init__(parent, players, "Place Standard Bet")
        self.setup_content()
        self.auto_resize_and_center()

    def setup_content(self):
        """Set up the dialog content."""
        # Title
        title = ctk.CTkLabel(self.dialog, text=f"🐎 Horse {self.horse} - {self.bet_type.title()}",
                            font=ctk.CTkFont(size=18, weight="bold"), text_color=RACING_COLORS["win"])
        title.pack(pady=(20, 10))

        # Bet info
        info_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        info_frame.pack(pady=10, padx=30, fill="x")

        if self.penalty > 0:
            info_text = f"🏆 Win: {self.multiplier}x multiplier\n💸 Lose: -${self.penalty} penalty"
            text_color = RACING_COLORS["warning"]
        else:
            info_text = f"🏆 Win: {self.multiplier}x multiplier\n✅ Lose: No penalty"
            text_color = RACING_COLORS["success"]

        info_label = ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=14), text_color=text_color)
        info_label.pack(pady=15)

        # Player selection
        player_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        player_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(player_frame, text="Select Player", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.player_var = ctk.StringVar()
        player_combo = ctk.CTkComboBox(player_frame, variable=self.player_var, values=list(self.players.keys()),
                                      font=ctk.CTkFont(size=12), state="readonly", width=250)
        player_combo.pack(pady=(0, 15))

        # Token selection
        token_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        token_frame.pack(pady=10, padx=30, fill="x")

        ctk.CTkLabel(token_frame, text="Select Token Value", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.token_var = ctk.StringVar()
        self.token_buttons = {}

        radio_frame = ctk.CTkFrame(token_frame, fg_color="transparent")
        radio_frame.pack(pady=(0, 15))

        for i, value in enumerate(["5", "3", "2", "1"]):
            btn = ctk.CTkRadioButton(radio_frame, text=f"${value} Token", variable=self.token_var,
                                   value=value, font=ctk.CTkFont(size=11))
            btn.grid(row=i//2, column=i%2, pady=5, padx=20, sticky="w")
            self.token_buttons[value] = btn

        self.player_var.trace("w", lambda *args: self.update_token_display())

        # Calculation display
        calc_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["surface"])
        calc_frame.pack(pady=10, padx=30, fill="x")

        self.calculation_label = ctk.CTkLabel(calc_frame, text="Select a token to see potential payout",
                                            font=ctk.CTkFont(size=12), text_color=RACING_COLORS["accent"])
        self.calculation_label.pack(pady=10)

        self.token_var.trace("w", lambda *args: self.update_calculation())

        # Buttons
        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=30, fill="x")

        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy,
                                  fg_color=RACING_COLORS["locked"], font=ctk.CTkFont(size=14))
        cancel_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        place_btn = ctk.CTkButton(button_frame, text="🎲 Place Bet", command=self.place_bet_action,
                                 fg_color=RACING_COLORS["success"], font=ctk.CTkFont(size=14, weight="bold"))
        place_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

    def update_token_display(self):
        """Update token button states."""
        player = self.player_var.get()
        if player and player in self.players:
            for value in ["5", "3", "2", "1"]:
                available = self.players[player].get_available_tokens(value)
                btn = self.token_buttons[value]
                if available > 0:
                    btn.configure(state="normal", text=f"${value} Token ({available} available)")
                else:
                    btn.configure(state="disabled", text=f"${value} Token (none left)")

    def update_calculation(self):
        """Update the calculation display."""
        if self.token_var.get():
            token_value = int(self.token_var.get())
            potential_win = token_value * self.multiplier
            if self.penalty > 0:
                calc_text = f"💰 If WIN: +${potential_win} | 💸 If LOSE: -${self.penalty}"
                text_color = RACING_COLORS["warning"]
            else:
                calc_text = f"💰 If WIN: +${potential_win} | ✅ If LOSE: No penalty"
                text_color = RACING_COLORS["success"]
            self.calculation_label.configure(text=calc_text, text_color=text_color)
        else:
            self.calculation_label.configure(text="Select a token to see potential payout", text_color=RACING_COLORS["accent"])

    def place_bet_action(self):
        """Handle placing the bet."""
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
        self.dialog.destroy()


class ModernSpecialBetDialog(ModernBetDialog):
    """Modern dialog for placing special bets."""

    def __init__(self, parent, players: Dict, bet_name: str, multiplier: int):
        self.bet_name = bet_name
        self.multiplier = multiplier
        super().__init__(parent, players, "Place Special Bet")
        self.setup_content()
        self.auto_resize_and_center()

    def setup_content(self):
        """Set up the dialog content."""
        title = ctk.CTkLabel(self.dialog, text=f"👑 {self.bet_name}", font=ctk.CTkFont(size=18, weight="bold"), text_color="#f59e0b")
        title.pack(pady=(20, 10))

        info_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        info_frame.pack(pady=10, padx=30, fill="x")

        if self.bet_name == "7 Finishes 5th or Worse":
            info_text = f"🏆 Win: {self.multiplier}x multiplier\n✅ Lose: No penalty"
            text_color = RACING_COLORS["success"]
        else:
            info_text = f"🏆 Win: {self.multiplier}x multiplier\n💸 Lose: -$1 penalty"
            text_color = RACING_COLORS["warning"]

        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=14), text_color=text_color).pack(pady=15)

        player_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        player_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(player_frame, text="Select Player", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.player_var = ctk.StringVar()
        ctk.CTkComboBox(player_frame, variable=self.player_var, values=list(self.players.keys()),
                       font=ctk.CTkFont(size=12), state="readonly", width=250).pack(pady=(0, 15))

        token_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        token_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(token_frame, text="Select Token Value", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.token_var = ctk.StringVar()
        self.token_buttons = {}
        radio_frame = ctk.CTkFrame(token_frame, fg_color="transparent")
        radio_frame.pack(pady=(0, 15))

        for i, value in enumerate(["5", "3", "2", "1"]):
            btn = ctk.CTkRadioButton(radio_frame, text=f"${value} Token", variable=self.token_var, value=value, font=ctk.CTkFont(size=11))
            btn.grid(row=i//2, column=i%2, pady=5, padx=20, sticky="w")
            self.token_buttons[value] = btn

        self.player_var.trace("w", lambda *args: self.update_token_display())

        calc_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["surface"])
        calc_frame.pack(pady=10, padx=30, fill="x")
        self.calculation_label = ctk.CTkLabel(calc_frame, text="Select a token to see potential payout",
                                            font=ctk.CTkFont(size=12), text_color=RACING_COLORS["accent"])
        self.calculation_label.pack(pady=10)
        self.token_var.trace("w", lambda *args: self.update_calculation())

        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=30, fill="x")
        ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy,
                     fg_color=RACING_COLORS["locked"], font=ctk.CTkFont(size=14)).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(button_frame, text="👑 Place Special Bet", command=self.place_bet_action,
                     fg_color=RACING_COLORS["success"], font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", fill="x", expand=True, padx=(5, 0))

    def update_token_display(self):
        player = self.player_var.get()
        if player and player in self.players:
            for value in ["5", "3", "2", "1"]:
                available = self.players[player].get_available_tokens(value)
                btn = self.token_buttons[value]
                if available > 0:
                    btn.configure(state="normal", text=f"${value} Token ({available} available)")
                else:
                    btn.configure(state="disabled", text=f"${value} Token (none left)")

    def update_calculation(self):
        if self.token_var.get():
            token_value = int(self.token_var.get())
            potential_win = token_value * self.multiplier
            if self.bet_name == "7 Finishes 5th or Worse":
                calc_text = f"💰 If WIN: +${potential_win} | ✅ If LOSE: No penalty"
                text_color = RACING_COLORS["success"]
            else:
                calc_text = f"💰 If WIN: +${potential_win} | 💸 If LOSE: -$1"
                text_color = RACING_COLORS["warning"]
            self.calculation_label.configure(text=calc_text, text_color=text_color)
        else:
            self.calculation_label.configure(text="Select a token to see potential payout", text_color=RACING_COLORS["accent"])

    def place_bet_action(self):
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
        self.dialog.destroy()


class ModernPropBetDialog(ModernBetDialog):
    """Modern dialog for placing prop bets."""

    def __init__(self, parent, players: Dict, prop_bet: Dict):
        self.prop_bet = prop_bet
        super().__init__(parent, players, "Place Prop Bet")
        self.setup_content()
        self.auto_resize_and_center()

    def setup_content(self):
        title = ctk.CTkLabel(self.dialog, text="🎯 Proposition Bet", font=ctk.CTkFont(size=18, weight="bold"), text_color=RACING_COLORS["prop"])
        title.pack(pady=(20, 10))

        desc_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        desc_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(desc_frame, text=self.prop_bet["description"], font=ctk.CTkFont(size=14, weight="bold"), wraplength=300).pack(pady=15)
        info_text = f"🏆 Win: {self.prop_bet['multiplier']}x multiplier\n💸 Lose: -${self.prop_bet['penalty']} penalty"
        ctk.CTkLabel(desc_frame, text=info_text, font=ctk.CTkFont(size=12), text_color=RACING_COLORS["warning"]).pack(pady=(0, 15))

        player_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        player_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(player_frame, text="Select Player", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.player_var = ctk.StringVar()
        ctk.CTkComboBox(player_frame, variable=self.player_var, values=list(self.players.keys()),
                       font=ctk.CTkFont(size=12), state="readonly", width=250).pack(pady=(0, 15))

        token_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        token_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(token_frame, text="Select Token Value", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.token_var = ctk.StringVar()
        self.token_buttons = {}
        radio_frame = ctk.CTkFrame(token_frame, fg_color="transparent")
        radio_frame.pack(pady=(0, 15))

        for i, value in enumerate(["5", "3", "2", "1"]):
            btn = ctk.CTkRadioButton(radio_frame, text=f"${value} Token", variable=self.token_var, value=value, font=ctk.CTkFont(size=11))
            btn.grid(row=i//2, column=i%2, pady=5, padx=20, sticky="w")
            self.token_buttons[value] = btn

        self.player_var.trace("w", lambda *args: self.update_token_display())

        calc_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["surface"])
        calc_frame.pack(pady=10, padx=30, fill="x")
        self.calculation_label = ctk.CTkLabel(calc_frame, text="Select a token to see potential payout", font=ctk.CTkFont(size=12), text_color=RACING_COLORS["accent"])
        self.calculation_label.pack(pady=10)
        self.token_var.trace("w", lambda *args: self.update_calculation())

        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=30, fill="x")
        ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy, fg_color=RACING_COLORS["locked"], font=ctk.CTkFont(size=14)).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(button_frame, text="🎯 Place Prop Bet", command=self.place_bet_action, fg_color=RACING_COLORS["success"], font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", fill="x", expand=True, padx=(5, 0))

    def update_token_display(self):
        player = self.player_var.get()
        if player and player in self.players:
            for value in ["5", "3", "2", "1"]:
                available = self.players[player].get_available_tokens(value)
                btn = self.token_buttons[value]
                if available > 0:
                    btn.configure(state="normal", text=f"${value} Token ({available} available)")
                else:
                    btn.configure(state="disabled", text=f"${value} Token (none left)")

    def update_calculation(self):
        if self.token_var.get():
            token_value = int(self.token_var.get())
            potential_win = token_value * self.prop_bet["multiplier"]
            calc_text = f"💰 If WIN: +${potential_win} | 💸 If LOSE: -${self.prop_bet['penalty']}"
            self.calculation_label.configure(text=calc_text, text_color=RACING_COLORS["prop"])
        else:
            self.calculation_label.configure(text="Select a token to see potential payout", text_color=RACING_COLORS["accent"])

    def place_bet_action(self):
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
        self.result = {"player": player, "token_value": int(token_value), "prop_bet_id": self.prop_bet["id"]}
        self.dialog.destroy()


class ModernExoticFinishDialog(ModernBetDialog):
    """Modern dialog for placing exotic finish bets."""

    def __init__(self, parent, players: Dict, exotic_finish: Dict):
        self.exotic_finish = exotic_finish
        super().__init__(parent, players, "Place Exotic Finish Bet")
        self.setup_content()
        self.auto_resize_and_center()

    def setup_content(self):
        title = ctk.CTkLabel(self.dialog, text="⭐ Exotic Finish Bet", font=ctk.CTkFont(size=18, weight="bold"), text_color=RACING_COLORS["exotic"])
        title.pack(pady=(20, 10))

        info_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        info_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(info_frame, text=self.exotic_finish["name"], font=ctk.CTkFont(size=16, weight="bold"), text_color=RACING_COLORS["exotic"]).pack(pady=(15, 5))
        ctk.CTkLabel(info_frame, text=self.exotic_finish["description"], font=ctk.CTkFont(size=12), wraplength=350).pack(pady=5)
        info_text = f"🏆 Win: {self.exotic_finish['multiplier']}x multiplier\n💸 Lose: -${self.exotic_finish['penalty']} penalty"
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=12), text_color=RACING_COLORS["warning"]).pack(pady=(5, 15))

        player_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        player_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(player_frame, text="Select Player", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.player_var = ctk.StringVar()
        ctk.CTkComboBox(player_frame, variable=self.player_var, values=list(self.players.keys()), font=ctk.CTkFont(size=12), state="readonly", width=250).pack(pady=(0, 15))

        token_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["card"])
        token_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(token_frame, text="Select Token Value", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))

        self.token_var = ctk.StringVar()
        self.token_buttons = {}
        radio_frame = ctk.CTkFrame(token_frame, fg_color="transparent")
        radio_frame.pack(pady=(0, 15))

        for i, value in enumerate(["5", "3", "2", "1"]):
            btn = ctk.CTkRadioButton(radio_frame, text=f"${value} Token", variable=self.token_var, value=value, font=ctk.CTkFont(size=11))
            btn.grid(row=i//2, column=i%2, pady=5, padx=20, sticky="w")
            self.token_buttons[value] = btn

        self.player_var.trace("w", lambda *args: self.update_token_display())

        calc_frame = ctk.CTkFrame(self.dialog, fg_color=RACING_COLORS["surface"])
        calc_frame.pack(pady=10, padx=30, fill="x")
        self.calculation_label = ctk.CTkLabel(calc_frame, text="Select a token to see potential payout", font=ctk.CTkFont(size=12), text_color=RACING_COLORS["accent"])
        self.calculation_label.pack(pady=10)
        self.token_var.trace("w", lambda *args: self.update_calculation())

        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=20, padx=30, fill="x")
        ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy, fg_color=RACING_COLORS["locked"], font=ctk.CTkFont(size=14)).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(button_frame, text="⭐ Place Exotic Bet", command=self.place_bet_action, fg_color=RACING_COLORS["success"], font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", fill="x", expand=True, padx=(5, 0))

    def update_token_display(self):
        player = self.player_var.get()
        if player and player in self.players:
            for value in ["5", "3", "2", "1"]:
                available = self.players[player].get_available_tokens(value)
                btn = self.token_buttons[value]
                if available > 0:
                    btn.configure(state="normal", text=f"${value} Token ({available} available)")
                else:
                    btn.configure(state="disabled", text=f"${value} Token (none left)")

    def update_calculation(self):
        if self.token_var.get():
            token_value = int(self.token_var.get())
            potential_win = token_value * self.exotic_finish["multiplier"]
            calc_text = f"💰 If WIN: +${potential_win} | 💸 If LOSE: -${self.exotic_finish['penalty']}"
            self.calculation_label.configure(text=calc_text, text_color=RACING_COLORS["exotic"])
        else:
            self.calculation_label.configure(text="Select a token to see potential payout", text_color=RACING_COLORS["accent"])

    def place_bet_action(self):
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
        self.result = {"player": player, "token_value": int(token_value), "exotic_finish_id": self.exotic_finish["id"]}
        self.dialog.destroy()


class ModernAddPlayerDialog:
    """Modern dialog for adding players."""

    def __init__(self, parent, existing_players: List[str]):
        self.parent = parent
        self.existing_players = existing_players
        self.result = None
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the modern dialog."""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Add New Player")
        self.dialog.geometry("400x200")
        self.dialog.configure(fg_color=RACING_COLORS["surface"])
        self.dialog.transient(self.parent)
        self.dialog.grab_set()

        ctk.CTkLabel(self.dialog, text="👤 Add New Player", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.dialog, text="Player Name:", font=ctk.CTkFont(size=14)).pack(pady=(0, 5))

        self.name_entry = ctk.CTkEntry(self.dialog, font=ctk.CTkFont(size=14), width=300, height=35)
        self.name_entry.pack(pady=(0, 20))
        self.name_entry.focus()

        button_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy, fg_color=RACING_COLORS["locked"],
                     font=ctk.CTkFont(size=14), width=120).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="➕ Add Player", command=self.add_player_action, fg_color=RACING_COLORS["success"],
                     font=ctk.CTkFont(size=14), width=120).pack(side="right", padx=10)

        self.dialog.bind('<Return>', lambda e: self.add_player_action())
        self.center_dialog()
        self.dialog.wait_window()

    def add_player_action(self):
        """Handle adding a player."""
        name = self.name_entry.get().strip()
        if name and name not in self.existing_players:
            self.result = name
            self.dialog.destroy()
        elif name in self.existing_players:
            messagebox.showerror("Error", "Player already exists!")
        else:
            messagebox.showerror("Error", "Please enter a valid name!")

    def center_dialog(self):
        """Center the dialog on parent."""
        self.dialog.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        self.dialog.geometry(f"+{x}+{y}")


class ModernRaceResultsDialog:
    """Modern dialog for entering race results."""

    def __init__(self, parent, horses: List[str], prop_bets: List[Dict], exotic_finishes: List[Dict], current_bets: Dict):
        self.parent = parent
        self.horses = horses
        self.prop_bets = prop_bets
        self.exotic_finishes = exotic_finishes
        self.current_bets = current_bets
        self.result = None
        self.setup_dialog()

    def setup_dialog(self):
        """Set up the modern dialog."""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("🏁 Enter Race Results")
        self.dialog.geometry("600x700")
        self.dialog.configure(fg_color=RACING_COLORS["surface"])
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.center_dialog()
        self.create_content()

    def create_content(self):
        """Create the dialog content."""
        main_frame = ctk.CTkScrollableFrame(self.dialog, fg_color=RACING_COLORS["surface"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(main_frame, text="🏁 Enter Race Results", font=ctk.CTkFont(size=20, weight="bold"), text_color=RACING_COLORS["win"]).pack(pady=(0, 20))

        # Horse results section
        horse_frame = ctk.CTkFrame(main_frame, fg_color=RACING_COLORS["card"])
        horse_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(horse_frame, text="🐎 Horse Finishing Positions", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 10))
        ctk.CTkLabel(horse_frame, text="Enter horses separated by commas (e.g., 7,2/3,11/12)",
                    font=ctk.CTkFont(size=12), text_color=RACING_COLORS["accent"]).pack(pady=(0, 15))

        self.entries = {}
        for position in ["Win (1st)", "Place (1st-2nd)", "Show (1st-3rd)"]:
            entry_frame = ctk.CTkFrame(horse_frame, fg_color="transparent")
            entry_frame.pack(fill="x", padx=20, pady=5)

            ctk.CTkLabel(entry_frame, text=f"{position}:", font=ctk.CTkFont(size=14, weight="bold"), width=120).pack(side="left", padx=(0, 10))
            entry = ctk.CTkEntry(entry_frame, font=ctk.CTkFont(size=12), placeholder_text=f"Enter {position.lower()} horses...")
            entry.pack(side="left", fill="x", expand=True)
            self.entries[position] = entry

        ctk.CTkLabel(horse_frame, text=f"Available horses: {', '.join(self.horses)}",
                    font=ctk.CTkFont(size=10), text_color=RACING_COLORS["accent"]).pack(pady=(10, 15))

        # Prop bets section
        prop_bets_with_bets = self._get_prop_bets_with_bets()
        self.prop_vars = {}

        if prop_bets_with_bets:
            prop_frame = ctk.CTkFrame(main_frame, fg_color=RACING_COLORS["card"])
            prop_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(prop_frame, text="🎯 Proposition Bet Results", font=ctk.CTkFont(size=16, weight="bold"), text_color=RACING_COLORS["prop"]).pack(pady=(15, 10))

            for prop_bet in prop_bets_with_bets:
                bet_frame = ctk.CTkFrame(prop_frame, fg_color=RACING_COLORS["surface"])
                bet_frame.pack(fill="x", padx=20, pady=5)

                ctk.CTkLabel(bet_frame, text=prop_bet["description"], font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=15, pady=(10, 5))

                var = ctk.StringVar()
                result_frame = ctk.CTkFrame(bet_frame, fg_color="transparent")
                result_frame.pack(anchor="w", padx=15, pady=(0, 10))

                ctk.CTkRadioButton(result_frame, text="✅ Won", variable=var, value="won", font=ctk.CTkFont(size=11)).pack(side="left", padx=(0, 20))
                ctk.CTkRadioButton(result_frame, text="❌ Lost", variable=var, value="lost", font=ctk.CTkFont(size=11)).pack(side="left")

                self.prop_vars[prop_bet["id"]] = var

            ctk.CTkLabel(prop_frame, text="").pack(pady=(0, 15))

        # Exotic finishes section
        exotic_finishes_with_bets = self._get_exotic_finishes_with_bets()
        self.exotic_vars = {}

        if exotic_finishes_with_bets:
            exotic_frame = ctk.CTkFrame(main_frame, fg_color=RACING_COLORS["card"])
            exotic_frame.pack(fill="x", pady=(0, 20))

            ctk.CTkLabel(exotic_frame, text="⭐ Exotic Finish Results", font=ctk.CTkFont(size=16, weight="bold"), text_color=RACING_COLORS["exotic"]).pack(pady=(15, 10))

            for exotic_finish in exotic_finishes_with_bets:
                bet_frame = ctk.CTkFrame(exotic_frame, fg_color=RACING_COLORS["surface"])
                bet_frame.pack(fill="x", padx=20, pady=5)

                ctk.CTkLabel(bet_frame, text=exotic_finish["name"], font=ctk.CTkFont(size=14, weight="bold"), text_color=RACING_COLORS["exotic"]).pack(anchor="w", padx=15, pady=(10, 5))
                ctk.CTkLabel(bet_frame, text=exotic_finish["description"], font=ctk.CTkFont(size=11), wraplength=400).pack(anchor="w", padx=15, pady=(0, 5))

                var = ctk.StringVar()
                result_frame = ctk.CTkFrame(bet_frame, fg_color="transparent")
                result_frame.pack(anchor="w", padx=15, pady=(0, 10))

                ctk.CTkRadioButton(result_frame, text="✅ Won", variable=var, value="won", font=ctk.CTkFont(size=11)).pack(side="left", padx=(0, 20))
                ctk.CTkRadioButton(result_frame, text="❌ Lost", variable=var, value="lost", font=ctk.CTkFont(size=11)).pack(side="left")

                self.exotic_vars[exotic_finish["id"]] = var

            ctk.CTkLabel(exotic_frame, text="").pack(pady=(0, 15))

        # Action buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)

        ctk.CTkButton(button_frame, text="Cancel", command=self.dialog.destroy, fg_color=RACING_COLORS["locked"],
                     font=ctk.CTkFont(size=14), height=40).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(button_frame, text="🏁 Process Results", command=self.process_results, fg_color=RACING_COLORS["success"],
                     font=ctk.CTkFont(size=14, weight="bold"), height=40).pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.dialog.wait_window()

    def process_results(self):
        """Process and validate the race results."""
        try:
            win_text = self.entries["Win (1st)"].get().strip()
            win_horses = [h.strip() for h in win_text.split(',') if h.strip()]
            place_text = self.entries["Place (1st-2nd)"].get().strip()
            place_horses = [h.strip() for h in place_text.split(',') if h.strip()]
            show_text = self.entries["Show (1st-3rd)"].get().strip()
            show_horses = [h.strip() for h in show_text.split(',') if h.strip()]

            all_horses = win_horses + place_horses + show_horses
            valid_horses = set(self.horses)
            if not all(h in valid_horses for h in all_horses):
                messagebox.showerror("Error", f"All horses must be one of: {', '.join(self.horses)}")
                return

            if not win_horses or not place_horses or not show_horses:
                messagebox.showerror("Error", "All position types must have at least one horse!")
                return

            prop_results = {}
            prop_bets_with_bets = self._get_prop_bets_with_bets()
            if prop_bets_with_bets:
                for prop_bet in prop_bets_with_bets:
                    prop_id = prop_bet["id"]
                    result = self.prop_vars[prop_id].get()
                    if result == "won":
                        prop_results[prop_id] = True
                    elif result == "lost":
                        prop_results[prop_id] = False
                    else:
                        messagebox.showerror("Error", f"Please select a result for prop bet: {prop_bet['description'][:30]}...")
                        return

            exotic_results = {}
            exotic_finishes_with_bets = self._get_exotic_finishes_with_bets()
            if exotic_finishes_with_bets:
                for exotic_finish in exotic_finishes_with_bets:
                    exotic_id = exotic_finish["id"]
                    result = self.exotic_vars[exotic_id].get()
                    if result == "won":
                        exotic_results[exotic_id] = True
                    elif result == "lost":
                        exotic_results[exotic_id] = False
                    else:
                        messagebox.showerror("Error", f"Please select a result for exotic finish: {exotic_finish['name']}")
                        return

            self.result = {
                "win": win_horses,
                "place": place_horses,
                "show": show_horses,
                "prop_results": prop_results,
                "exotic_results": exotic_results
            }
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Please enter valid data: {str(e)}")

    def center_dialog(self):
        """Center the dialog on parent."""
        self.dialog.update_idletasks()
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        self.dialog.geometry(f"+{x}+{y}")

    def _get_prop_bets_with_bets(self) -> List[Dict]:
        """Get only the prop bets that have actual bets placed on them."""
        prop_bets_with_bets = []
        prop_bet_ids_with_bets = set()
        for bet in self.current_bets.values():
            if bet.is_prop_bet():
                prop_bet_ids_with_bets.add(bet.prop_bet_id)
        for prop_bet in self.prop_bets:
            if prop_bet["id"] in prop_bet_ids_with_bets:
                prop_bets_with_bets.append(prop_bet)
        return prop_bets_with_bets

    def _get_exotic_finishes_with_bets(self) -> List[Dict]:
        """Get only the exotic finishes that have actual bets placed on them."""
        exotic_finishes_with_bets = []
        exotic_finish_ids_with_bets = set()
        for bet in self.current_bets.values():
            if bet.is_exotic_bet():
                exotic_finish_ids_with_bets.add(bet.exotic_finish_id)
        for exotic_finish in self.exotic_finishes:
            if exotic_finish["id"] in exotic_finish_ids_with_bets:
                exotic_finishes_with_bets.append(exotic_finish)
        return exotic_finishes_with_bets