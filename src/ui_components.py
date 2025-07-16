def _setup_current_bets(self, parent):
    """Set up the current bets display."""
    # Modern card container
    bets_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
    bets_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Title
    title_frame = tk.Frame(bets_container, bg=MODERN_COLORS["card"])
    title_frame.pack(fill="x", pady=(15, 10))

    title_label = tk.Label(title_frame, text="CURRENT BETS", font=("Segoe UI", 14, "bold"),
                           bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
    """UI components and widgets for the Ready Set Bet application."""


import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional
from .constants import COLORS, SPECIAL_BETS, HORSES, HORSE_COLORS, BETTING_GRID

# Modern color scheme
MODERN_COLORS = {
    "primary": "#2563eb",  # Modern blue
    "secondary": "#64748b",  # Slate gray
    "success": "#10b981",  # Emerald green
    "warning": "#f59e0b",  # Amber
    "danger": "#ef4444",  # Red
    "surface": "#f8fafc",  # Light gray background
    "card": "#ffffff",  # White cards
    "text_primary": "#1e293b",  # Dark text
    "text_secondary": "#64748b",  # Light text
    "border": "#e2e8f0",  # Light border
    "show": {
        "bg": "#cd7c2f",  # Modern copper
        "fg": "white",
        "hover": "#b8691a"
    },
    "place": {
        "bg": "#9ca3af",  # Modern silver
        "fg": "white",
        "hover": "#6b7280"
    },
    "win": {
        "bg": "#f59e0b",  # Modern gold
        "fg": "white",
        "hover": "#d97706"
    },
    "locked": {
        "bg": "#6b7280",  # Modern gray
        "fg": "white",
        "hover": "#4b5563"
    },
    "special": {
        "blue": {"bg": "#3b82f6", "fg": "white", "hover": "#2563eb"},
        "orange": {"bg": "#f97316", "fg": "white", "hover": "#ea580c"},
        "red": {"bg": "#ef4444", "fg": "white", "hover": "#dc2626"},
        "black": {"bg": "#374151", "fg": "white", "hover": "#1f2937"}
    },
    "prop": {
        "bg": "#8b5cf6",  # Modern purple
        "fg": "white",
        "hover": "#7c3aed"
    },
    "exotic": {
        "bg": "#f97316",  # Modern orange
        "fg": "white",
        "hover": "#ea580c"
    }
}


class BettingBoard:
    """Handles the betting board UI component."""

    def __init__(self, parent, on_standard_bet: Callable, on_special_bet: Callable, on_prop_bet: Callable,
                 on_exotic_bet: Callable):
        self.parent = parent
        self.on_standard_bet = on_standard_bet
        self.on_special_bet = on_special_bet
        self.on_prop_bet = on_prop_bet
        self.on_exotic_bet = on_exotic_bet
        self.bet_buttons = {}
        self.prop_bet_buttons = {}
        self.special_bet_buttons = {}
        self.exotic_finish_buttons = {}
        self.setup_board()

    def setup_board(self):
        """Set up the betting board UI."""
        # Main betting board frame with modern styling
        board_frame = ttk.Frame(self.parent)
        board_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Configure main grid layout: left side for betting board, right side for current bets
        board_frame.columnconfigure(0, weight=4)  # Left side gets more space for bigger betting grid
        board_frame.columnconfigure(1, weight=1)  # Right side for current bets
        board_frame.rowconfigure(0, weight=1)

        # Left side frame for all betting components
        left_frame = ttk.Frame(board_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))

        # Right side frame for current bets
        right_frame = ttk.Frame(board_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Setup betting components on the left
        self._setup_betting_components(left_frame)

        # Setup current bets on the right
        self._setup_current_bets(right_frame)

    def _setup_betting_components(self, parent):
        """Set up all betting components (prop bets, special bets, exotic finishes, main grid)."""
        # Prop bets (at the top)
        self._setup_prop_bets(parent)

        # Special bets
        self._setup_special_bets(parent)

        # Exotic finishes
        self._setup_exotic_finishes(parent)

        # Main betting grid
        self._setup_main_grid(parent)

    def _setup_prop_bets(self, parent):
        """Set up the prop bets section."""
        # Modern card-style frame
        self.prop_frame = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        self.prop_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="ew", padx=10)

        # Modern title
        title_frame = tk.Frame(self.prop_frame, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(title_frame, text="PROP BETS", font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Will be populated by update_prop_bets method

    def update_prop_bets(self, prop_bets: List[Dict]):
        """Update the prop bets display."""
        # Clear existing prop bet buttons completely
        for widget in self.prop_frame.winfo_children():
            widget.destroy()
        self.prop_bet_buttons.clear()

        # Recreate title
        title_frame = tk.Frame(self.prop_frame, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(title_frame, text="PROP BETS", font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        if not prop_bets:
            no_bets_label = tk.Label(self.prop_frame, text="No prop bets for this race",
                                     font=("Segoe UI", 10), bg=MODERN_COLORS["card"],
                                     fg=MODERN_COLORS["text_secondary"])
            no_bets_label.pack(pady=20)
            return

        # Container for buttons
        buttons_frame = tk.Frame(self.prop_frame, bg=MODERN_COLORS["card"])
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Create prop bet buttons with modern styling
        for i, prop_bet in enumerate(prop_bets):
            btn_text = f"{prop_bet['description']}\n{prop_bet['multiplier']}x\n(-${prop_bet['penalty']})"

            btn = tk.Button(buttons_frame, text=btn_text, font=("Segoe UI", 9, "bold"),
                            bg=MODERN_COLORS["prop"]["bg"], fg=MODERN_COLORS["prop"]["fg"],
                            activebackground=MODERN_COLORS["prop"]["hover"],
                            activeforeground=MODERN_COLORS["prop"]["fg"],
                            relief="flat", bd=0, wraplength=140, height=4,
                            cursor="hand2",
                            command=lambda pb=prop_bet: self.on_prop_bet(pb))
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            buttons_frame.columnconfigure(i, weight=1)
            self.prop_bet_buttons[prop_bet["id"]] = btn

            # Add subtle shadow effect with border
            btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

    def _setup_special_bets(self, parent):
        """Set up the special bets section."""
        # Modern card container
        special_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        special_container.grid(row=1, column=0, columnspan=3, pady=(0, 20), sticky="ew", padx=10)

        # Title
        title_frame = tk.Frame(special_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(title_frame, text="SPECIAL BETS", font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Buttons container
        special_frame = tk.Frame(special_container, bg=MODERN_COLORS["card"])
        special_frame.pack(fill="x", padx=15, pady=(0, 15))

        for i, (name, payout, color) in enumerate(SPECIAL_BETS):
            color_config = MODERN_COLORS["special"][color]

            # Only color bets have penalty, not the "7 Finishes 5th or Worse"
            if color in ["blue", "orange", "red"]:
                btn_text = f"{name}\n{payout}\n(-$1)"
            else:
                btn_text = f"{name}\n{payout}"

            btn = tk.Button(special_frame, text=btn_text, font=("Segoe UI", 10, "bold"),
                            bg=color_config["bg"], fg=color_config["fg"],
                            activebackground=color_config["hover"], activeforeground=color_config["fg"],
                            relief="flat", bd=0, height=3, cursor="hand2",
                            command=lambda n=name, p=int(payout[:-1]): self.on_special_bet(n, p))
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            special_frame.columnconfigure(i, weight=1)
            self.special_bet_buttons[name] = btn

            # Modern border
            btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

    def _setup_exotic_finishes(self, parent):
        """Set up the exotic finishes section."""
        # Modern card container
        self.exotic_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        self.exotic_container.grid(row=2, column=0, columnspan=3, pady=(0, 20), sticky="ew", padx=10)

        # Title
        title_frame = tk.Frame(self.exotic_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(title_frame, text="EXOTIC FINISHES", font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Container for exotic finish buttons
        self.exotic_frame = tk.Frame(self.exotic_container, bg=MODERN_COLORS["card"])
        self.exotic_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Will be populated by update_exotic_finishes method

    def update_exotic_finishes(self, exotic_finishes: List[Dict]):
        """Update the exotic finishes display."""
        # Clear existing exotic finish buttons completely
        for widget in self.exotic_frame.winfo_children():
            widget.destroy()
        self.exotic_finish_buttons.clear()

        if not exotic_finishes:
            no_exotic_label = tk.Label(self.exotic_frame, text="No exotic finishes available",
                                       font=("Segoe UI", 10), bg=MODERN_COLORS["card"],
                                       fg=MODERN_COLORS["text_secondary"])
            no_exotic_label.pack(pady=20)
            return

        # Create exotic finish buttons with modern styling
        for i, exotic_finish in enumerate(exotic_finishes):
            btn_text = f"{exotic_finish['name']}\n{exotic_finish['description']}\n{exotic_finish['multiplier']}x (-${exotic_finish['penalty']})\nUp to 3 players"

            btn = tk.Button(self.exotic_frame, text=btn_text, font=("Segoe UI", 9, "bold"),
                            bg=MODERN_COLORS["exotic"]["bg"], fg=MODERN_COLORS["exotic"]["fg"],
                            activebackground=MODERN_COLORS["exotic"]["hover"],
                            activeforeground=MODERN_COLORS["exotic"]["fg"],
                            relief="flat", bd=0, wraplength=200, height=5, cursor="hand2",
                            command=lambda ef=exotic_finish: self.on_exotic_bet(ef))
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.exotic_frame.columnconfigure(i, weight=1)
            self.exotic_finish_buttons[exotic_finish["id"]] = btn

            # Modern border
            btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

    def _setup_main_grid(self, parent):
        """Set up the main betting grid."""
        # Modern card container for betting grid
        grid_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        grid_container.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Title
        title_frame = tk.Frame(grid_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(title_frame, text="BETTING BOARD", font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Main betting frame
        main_frame = tk.Frame(grid_container, bg=MODERN_COLORS["card"])
        main_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

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
            ("SHOW", MODERN_COLORS["show"], 0, 2),
            ("PLACE", MODERN_COLORS["place"], 2, 2),
            ("WIN", MODERN_COLORS["win"], 4, 3)
        ]

        for text, color_config, col, span in headers:
            header = tk.Label(parent, text=text, font=("Segoe UI", 16, "bold"),
                              bg=color_config["bg"], fg=color_config["fg"],
                              relief="flat", bd=0, height=2)
            header.grid(row=0, column=col, columnspan=span, sticky="ew", padx=3, pady=3)

            # Modern border
            header.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

    def _setup_betting_buttons(self, parent):
        """Set up the betting buttons."""
        # Modern horse colors
        modern_horse_colors = {
            "2/3": "#3b82f6",  # Modern blue
            "4": "#3b82f6",  # Modern blue
            "5": "#f97316",  # Modern orange
            "6": "#ef4444",  # Modern red
            "7": "#374151",  # Modern black
            "8": "#ef4444",  # Modern red
            "9": "#f97316",  # Modern orange
            "10": "#3b82f6",  # Modern blue
            "11/12": "#3b82f6"  # Modern blue
        }

        for horse_idx, horse in enumerate(HORSES):
            row = horse_idx + 1

            # Modern horse label
            horse_label = tk.Label(parent, text=horse, font=("Segoe UI", 12, "bold"),
                                   bg=modern_horse_colors.get(horse, "#6b7280"), fg="white",
                                   width=8, height=2, relief="flat", bd=0)
            horse_label.grid(row=row, column=7, padx=3, pady=3, sticky="ew")
            horse_label.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

            # Betting spots
            horse_bets = BETTING_GRID[horse_idx]
            self.bet_buttons[horse] = {}

            for col_idx, (multiplier, penalty) in enumerate(horse_bets):
                bet_type = "show" if col_idx < 2 else "place" if col_idx < 4 else "win"
                color_config = MODERN_COLORS[bet_type]

                btn_text = f"{multiplier}x\n(-${penalty})" if penalty > 0 else f"{multiplier}x\n "

                btn = tk.Button(parent, text=btn_text, font=("Segoe UI", 11, "bold"),
                                bg=color_config["bg"], fg=color_config["fg"],
                                activebackground=color_config["hover"], activeforeground=color_config["fg"],
                                relief="flat", bd=0, width=6, height=2, cursor="hand2",
                                command=lambda h=horse, t=bet_type, m=multiplier, p=penalty, r=row, c=col_idx:
                                self.on_standard_bet(h, t, m, p, r, c))
                btn.grid(row=row, column=col_idx, padx=3, pady=3, sticky="ew")

                # Modern border
                btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

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
        # Modern card container
        bets_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        bets_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Title
        title_frame = tk.Frame(bets_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(15, 10))

        title_label = tk.Label(title_frame, text="CURRENT BETS", font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Treeview container
        tree_frame = tk.Frame(bets_container, bg=MODERN_COLORS["card"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        # Modern Treeview for bets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Modern.Treeview",
                        background=MODERN_COLORS["surface"],
                        foreground=MODERN_COLORS["text_primary"],
                        fieldbackground=MODERN_COLORS["surface"],
                        borderwidth=0,
                        relief="flat")
        style.configure("Modern.Treeview.Heading",
                        background=MODERN_COLORS["secondary"],
                        foreground="white",
                        borderwidth=0,
                        relief="flat")

        self.bets_tree = ttk.Treeview(tree_frame,
                                      columns=("Player", "Horse", "Type", "Token", "Win", "Lose", "Remove"),
                                      show="headings", height=15, style="Modern.Treeview")

        # Configure columns with modern styling
        columns = [
            ("Player", 80), ("Horse", 60), ("Type", 80), ("Token", 60),
            ("Win", 60), ("Lose", 60), ("Remove", 70)
        ]

        for col, width in columns:
            self.bets_tree.heading(col, text=col)
            self.bets_tree.column(col, width=width)

        # Modern scrollbar
        bets_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.bets_tree.yview)
        self.bets_tree.configure(yscrollcommand=bets_scrollbar.set)

        self.bets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        bets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Modern buttons
        button_frame = tk.Frame(bets_container, bg=MODERN_COLORS["card"])
        button_frame.pack(pady=(5, 15), fill="x", padx=15)

        self.remove_btn = tk.Button(button_frame, text="Remove Selected Bet",
                                    font=("Segoe UI", 10, "bold"),
                                    bg=MODERN_COLORS["danger"], fg="white",
                                    activebackground="#dc2626", activeforeground="white",
                                    relief="flat", bd=0, height=2, cursor="hand2")
        self.remove_btn.pack(side=tk.TOP, pady=(0, 5), fill="x")

        self.clear_btn = tk.Button(button_frame, text="Clear All Bets",
                                   font=("Segoe UI", 10, "bold"),
                                   bg=MODERN_COLORS["secondary"], fg="white",
                                   activebackground="#475569", activeforeground="white",
                                   relief="flat", bd=0, height=2, cursor="hand2")
        self.clear_btn.pack(side=tk.TOP, fill="x")

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
                        bg=MODERN_COLORS["locked"]["bg"],
                        fg=MODERN_COLORS["locked"]["fg"],
                        activebackground=MODERN_COLORS["locked"]["hover"],
                        activeforeground=MODERN_COLORS["locked"]["fg"],
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
                bg=MODERN_COLORS["locked"]["bg"],
                fg=MODERN_COLORS["locked"]["fg"],
                activebackground=MODERN_COLORS["locked"]["hover"],
                activeforeground=MODERN_COLORS["locked"]["fg"],
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
                bg=MODERN_COLORS["locked"]["bg"],
                fg=MODERN_COLORS["locked"]["fg"],
                activebackground=MODERN_COLORS["locked"]["hover"],
                activeforeground=MODERN_COLORS["locked"]["fg"],
                state="disabled"
            )

    def update_exotic_finish_appearance(self, exotic_finish_id: int, players: List[str]):
        """Update exotic finish button appearance to show players who bet on it."""
        if exotic_finish_id in self.exotic_finish_buttons:
            button = self.exotic_finish_buttons[exotic_finish_id]
            current_text = button.cget("text")
            lines = current_text.split('\n')

            # Keep the first 4 lines (name, description, multiplier, "Up to 3 players")
            if len(lines) >= 4:
                player_text = ", ".join([p[:6] for p in players])
                new_text = f"{lines[0]}\n{lines[1]}\n{lines[2]}\n{player_text}"
            else:
                player_text = ", ".join([p[:6] for p in players])
                new_text = f"{current_text}\n{player_text}"

            # Change color if 3 players have bet (fully locked)
            if len(players) >= 3:
                button.configure(
                    text=new_text,
                    bg=MODERN_COLORS["locked"]["bg"],
                    fg=MODERN_COLORS["locked"]["fg"],
                    activebackground=MODERN_COLORS["locked"]["hover"],
                    activeforeground=MODERN_COLORS["locked"]["fg"],
                    state="disabled"
                )
            else:
                button.configure(text=new_text)

    def reset_button_appearance(self, horse: str, bet_type: str, row: int, col: int):
        """Reset button to original appearance."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]
                    penalty = btn_info["penalty"]

                    color_config = MODERN_COLORS[bet_type]
                    btn_text = f"{multiplier}x\n(-${penalty})" if penalty > 0 else f"{multiplier}x\n "

                    button.configure(
                        text=btn_text,
                        bg=color_config["bg"],
                        fg=color_config["fg"],
                        activebackground=color_config["hover"],
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
                    color_config = MODERN_COLORS["special"][color]

                    if color in ["blue", "orange", "red"]:
                        btn_text = f"{name}\n{payout}\n(-$1)"
                    else:
                        btn_text = f"{name}\n{payout}"

                    button.configure(
                        text=btn_text,
                        bg=color_config["bg"],
                        fg=color_config["fg"],
                        activebackground=color_config["hover"],
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
                bg=MODERN_COLORS["prop"]["bg"],
                fg=MODERN_COLORS["prop"]["fg"],
                activebackground=MODERN_COLORS["prop"]["hover"],
                activeforeground=MODERN_COLORS["prop"]["fg"],
                state="normal"
            )

    def reset_exotic_finish_appearance(self, exotic_finish_id: int, exotic_finish: Dict):
        """Reset exotic finish button to original appearance."""
        if exotic_finish_id in self.exotic_finish_buttons:
            button = self.exotic_finish_buttons[exotic_finish_id]
            btn_text = f"{exotic_finish['name']}\n{exotic_finish['description']}\n{exotic_finish['multiplier']}x (-${exotic_finish['penalty']})\nUp to 3 players"

            button.configure(
                text=btn_text,
                bg=MODERN_COLORS["exotic"]["bg"],
                fg=MODERN_COLORS["exotic"]["fg"],
                activebackground=MODERN_COLORS["exotic"]["hover"],
                activeforeground=MODERN_COLORS["exotic"]["fg"],
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
                        if button.cget("bg") != MODERN_COLORS["locked"]["bg"]:
                            button.configure(state="normal")
                    else:
                        button.configure(state="disabled")

        # Special bet buttons
        for button in self.special_bet_buttons.values():
            if enabled:
                # Only enable if not already locked
                if button.cget("bg") != MODERN_COLORS["locked"]["bg"]:
                    button.configure(state="normal")
            else:
                button.configure(state="disabled")

        # Prop bet buttons
        for button in self.prop_bet_buttons.values():
            if enabled:
                # Only enable if not already locked
                if button.cget("bg") != MODERN_COLORS["locked"]["bg"]:
                    button.configure(state="normal")
            else:
                button.configure(state="disabled")

        # Exotic finish buttons
        for button in self.exotic_finish_buttons.values():
            if enabled:
                # Only enable if not already fully locked (3 players)
                if button.cget("bg") != MODERN_COLORS["locked"]["bg"]:
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

    def reset_exotic_finishes_to_orange(self, exotic_finishes: List[Dict]):
        """Reset exotic finish buttons to their original orange appearance with full data."""
        for exotic_finish in exotic_finishes:
            if exotic_finish["id"] in self.exotic_finish_buttons:
                self.reset_exotic_finish_appearance(exotic_finish["id"], exotic_finish)

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
            elif bet.is_exotic_bet():
                horse_display = "Exotic"
                type_display = f"Exotic #{bet.exotic_finish_id}"
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