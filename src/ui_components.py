def _setup_current_bets(self, parent):
    """Set up the current bets display with racing theme - compact and responsive."""
    """UI components and widgets for the Ready Set Bet application."""


import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Callable, Optional
from .constants import COLORS, SPECIAL_BETS, HORSES, HORSE_COLORS, BETTING_GRID

# Ultra-modern horse racing themed color scheme
MODERN_COLORS = {
    "primary": "#1e40af",  # Deep racing blue
    "secondary": "#475569",  # Slate gray
    "success": "#059669",  # Emerald green
    "warning": "#d97706",  # Amber
    "danger": "#dc2626",  # Red
    "surface": "#f1f5f9",  # Very light gray background
    "card": "#ffffff",  # Pure white cards
    "text_primary": "#0f172a",  # Very dark text
    "text_secondary": "#64748b",  # Muted text
    "border": "#e2e8f0",  # Light border
    "accent": "#8b5cf6",  # Purple accent
    "track": "#0f172a",  # Dark track color

    # Racing-themed betting colors with gradients
    "show": {
        "bg": "#cd7c2f",  # Bronze/Copper
        "fg": "white",
        "hover": "#b8691a",
        "shadow": "#a0591a"
    },
    "place": {
        "bg": "#71717a",  # Silver
        "fg": "white",
        "hover": "#52525b",
        "shadow": "#3f3f46"
    },
    "win": {
        "bg": "#eab308",  # Gold
        "fg": "#1f2937",
        "hover": "#ca8a04",
        "shadow": "#a16207"
    },
    "locked": {
        "bg": "#6b7280",
        "fg": "white",
        "hover": "#4b5563"
    },

    # Horse colors (matching track silks)
    "horse_silks": {
        "2/3": {"bg": "#2563eb", "accent": "#60a5fa"},  # Royal Blue
        "4": {"bg": "#1d4ed8", "accent": "#3b82f6"},  # Blue
        "5": {"bg": "#ea580c", "accent": "#fb923c"},  # Orange
        "6": {"bg": "#dc2626", "accent": "#f87171"},  # Red
        "7": {"bg": "#1f2937", "accent": "#6b7280"},  # Black
        "8": {"bg": "#b91c1c", "accent": "#ef4444"},  # Crimson
        "9": {"bg": "#c2410c", "accent": "#f97316"},  # Orange-Red
        "10": {"bg": "#1e40af", "accent": "#3b82f6"},  # Navy Blue
        "11/12": {"bg": "#1e3a8a", "accent": "#60a5fa"}  # Deep Blue
    },

    "special": {
        "blue": {"bg": "#3b82f6", "fg": "white", "hover": "#2563eb"},
        "orange": {"bg": "#f97316", "fg": "white", "hover": "#ea580c"},
        "red": {"bg": "#ef4444", "fg": "white", "hover": "#dc2626"},
        "black": {"bg": "#374151", "fg": "white", "hover": "#1f2937"}
    },
    "prop": {
        "bg": "#8b5cf6",  # Purple with racing flair
        "fg": "white",
        "hover": "#7c3aed",
        "shadow": "#6d28d9"
    },
    "exotic": {
        "bg": "#f59e0b",  # Golden yellow
        "fg": "white",
        "hover": "#d97706",
        "shadow": "#b45309"
    }
}

# Racing track patterns and decorative elements
TRACK_PATTERNS = {
    "checkered": "🏁",
    "horse": "🐎",
    "trophy": "🏆",
    "star": "⭐",
    "diamond": "💎",
    "crown": "👑"
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
        """Set up the betting board UI with racing theme - fully responsive."""
        # Main betting board frame with racing-inspired styling
        board_frame = ttk.Frame(self.parent)
        board_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Configure main grid layout - responsive
        board_frame.columnconfigure(0, weight=4)  # Left side for betting board
        board_frame.columnconfigure(1, weight=1)  # Right side for current bets
        board_frame.rowconfigure(0, weight=1)

        # Left side frame with racing track styling - responsive
        left_frame = tk.Frame(board_frame, bg=MODERN_COLORS["surface"], relief="flat", bd=0)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_frame.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["track"])

        # Make left frame responsive
        left_frame.rowconfigure(3, weight=1)  # Main grid gets remaining space

        # Right side frame for current bets - responsive
        right_frame = tk.Frame(board_frame, bg=MODERN_COLORS["surface"], relief="flat", bd=0)
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["track"])

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
        """Set up the prop bets section with racing theme - compact and responsive."""
        # Racing-themed card with minimal padding
        self.prop_frame = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        self.prop_frame.grid(row=0, column=0, columnspan=3, pady=(5, 8), sticky="ew", padx=10)

        # Add racing-inspired border
        self.prop_frame.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["accent"])

        # Compact racing-themed title
        title_frame = tk.Frame(self.prop_frame, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(8, 5))

        # Smaller title without horse emoji
        title_label = tk.Label(title_frame, text="PROPOSITION BETS",
                               font=("Segoe UI", 12, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Will be populated by update_prop_bets method

    def update_prop_bets(self, prop_bets: List[Dict]):
        """Update the prop bets display with racing theme - better readability."""
        # Clear existing prop bet buttons completely
        for widget in self.prop_frame.winfo_children():
            widget.destroy()
        self.prop_bet_buttons.clear()

        # Recreate compact racing-themed title
        title_frame = tk.Frame(self.prop_frame, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(8, 5))

        title_label = tk.Label(title_frame, text=f"{TRACK_PATTERNS['horse']} PROPOSITION BETS",
                               font=("Segoe UI", 12, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        if not prop_bets:
            no_bets_label = tk.Label(self.prop_frame, text="🏁 No proposition bets available",
                                     font=("Segoe UI", 9), bg=MODERN_COLORS["card"],
                                     fg=MODERN_COLORS["text_secondary"])
            no_bets_label.pack(pady=10)
            return

        # Container for buttons - better sizing
        buttons_frame = tk.Frame(self.prop_frame, bg=MODERN_COLORS["card"])
        buttons_frame.pack(fill="x", padx=10, pady=(0, 8))

        # Create better sized prop bet buttons - no truncation
        for i, prop_bet in enumerate(prop_bets):
            btn_text = f"{prop_bet['description']}\n{prop_bet['multiplier']}x | -${prop_bet['penalty']}"

            btn = tk.Button(buttons_frame, text=btn_text, font=("Segoe UI", 8, "bold"),
                            bg=MODERN_COLORS["prop"]["bg"], fg=MODERN_COLORS["prop"]["fg"],
                            activebackground=MODERN_COLORS["prop"]["hover"],
                            activeforeground=MODERN_COLORS["prop"]["fg"],
                            relief="flat", bd=0, wraplength=150, height=4,
                            cursor="hand2",
                            command=lambda pb=prop_bet: self.on_prop_bet(pb))
            btn.grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            buttons_frame.columnconfigure(i, weight=1)
            self.prop_bet_buttons[prop_bet["id"]] = btn

            # Subtle border
            btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["prop"]["shadow"])

    def _setup_special_bets(self, parent):
        """Set up the special bets section with racing theme - better readability."""
        # Compact racing-themed card container
        special_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        special_container.grid(row=1, column=0, columnspan=3, pady=(0, 8), sticky="ew", padx=10)
        special_container.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["primary"])

        # Compact title
        title_frame = tk.Frame(special_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(8, 5))

        title_label = tk.Label(title_frame, text=f"{TRACK_PATTERNS['crown']} SPECIAL RACING BETS",
                               font=("Segoe UI", 12, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Buttons container - better sizing
        special_frame = tk.Frame(special_container, bg=MODERN_COLORS["card"])
        special_frame.pack(fill="x", padx=10, pady=(0, 8))

        for i, (name, payout, color) in enumerate(SPECIAL_BETS):
            color_config = MODERN_COLORS["special"][color]

            # Better readable button text
            if color in ["blue", "orange", "red"]:
                btn_text = f"{name}\n{payout} | -$1"
            else:
                btn_text = f"{name}\n{payout} | FREE"

            btn = tk.Button(special_frame, text=btn_text, font=("Segoe UI", 9, "bold"),
                            bg=color_config["bg"], fg=color_config["fg"],
                            activebackground=color_config["hover"], activeforeground=color_config["fg"],
                            relief="flat", bd=0, height=3, cursor="hand2",
                            command=lambda n=name, p=int(payout[:-1]): self.on_special_bet(n, p))
            btn.grid(row=0, column=i, padx=4, pady=4, sticky="ew")
            special_frame.columnconfigure(i, weight=1)
            self.special_bet_buttons[name] = btn

            # Subtle border
            btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["track"])

    def _setup_exotic_finishes(self, parent):
        """Set up the exotic finishes section with racing theme - compact version."""
        # Compact racing-themed card container
        self.exotic_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        self.exotic_container.grid(row=2, column=0, columnspan=3, pady=(0, 8), sticky="ew", padx=10)
        self.exotic_container.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["warning"])

        # Compact title
        title_frame = tk.Frame(self.exotic_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(8, 5))

        title_label = tk.Label(title_frame, text=f"{TRACK_PATTERNS['star']} EXOTIC FINISH BETS",
                               font=("Segoe UI", 12, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Container for exotic finish buttons - more compact
        self.exotic_frame = tk.Frame(self.exotic_container, bg=MODERN_COLORS["card"])
        self.exotic_frame.pack(fill="x", padx=10, pady=(0, 8))

        # Will be populated by update_exotic_finishes method

    def update_exotic_finishes(self, exotic_finishes: List[Dict]):
        """Update the exotic finishes display with racing theme - compact version."""
        # Clear existing exotic finish buttons completely
        for widget in self.exotic_frame.winfo_children():
            widget.destroy()
        self.exotic_finish_buttons.clear()

        if not exotic_finishes:
            no_exotic_label = tk.Label(self.exotic_frame,
                                       text=f"{TRACK_PATTERNS['checkered']} No exotic finish bets available",
                                       font=("Segoe UI", 9), bg=MODERN_COLORS["card"],
                                       fg=MODERN_COLORS["text_secondary"])
            no_exotic_label.pack(pady=10)
            return

        # Create compact exotic finish buttons
        for i, exotic_finish in enumerate(exotic_finishes):
            btn_text = f"🏆 {exotic_finish['name']}\n{exotic_finish['description'][:25]}...\n💰 {exotic_finish['multiplier']}x | 💸 -${exotic_finish['penalty']} | 🏇 Up to 3"

            btn = tk.Button(self.exotic_frame, text=btn_text, font=("Segoe UI", 8, "bold"),
                            bg=MODERN_COLORS["exotic"]["bg"], fg=MODERN_COLORS["exotic"]["fg"],
                            activebackground=MODERN_COLORS["exotic"]["hover"],
                            activeforeground=MODERN_COLORS["exotic"]["fg"],
                            relief="flat", bd=0, wraplength=150, height=4, cursor="hand2",
                            command=lambda ef=exotic_finish: self.on_exotic_bet(ef))
            btn.grid(row=0, column=i, padx=3, pady=3, sticky="ew")
            self.exotic_frame.columnconfigure(i, weight=1)
            self.exotic_finish_buttons[exotic_finish["id"]] = btn

            # Subtle border
            btn.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["exotic"]["shadow"])

    def _setup_main_grid(self, parent):
        """Set up the main betting grid with racing theme - responsive and compact."""
        # Racing track-themed container for betting grid - responsive
        grid_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        grid_container.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0, 5))
        grid_container.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["track"])

        # Configure for responsiveness
        grid_container.rowconfigure(1, weight=1)  # Main frame gets remaining space

        # Compact racing-themed title
        title_frame = tk.Frame(grid_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(8, 5))

        title_label = tk.Label(title_frame, text=f"{TRACK_PATTERNS['checkered']} RACING ODDS BOARD",
                               font=("Segoe UI", 14, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        # Main betting frame with track styling - responsive
        main_frame = tk.Frame(grid_container, bg=MODERN_COLORS["surface"])
        main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 8))
        main_frame.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

        # Headers
        self._setup_headers(main_frame)

        # Betting buttons
        self._setup_betting_buttons(main_frame)

        # Configure grid weights for responsiveness
        for i in range(8):
            main_frame.columnconfigure(i, weight=1)

    def _setup_headers(self, parent):
        """Set up the column headers with racing theme - better readability."""
        headers = [
            ("🥉 SHOW", MODERN_COLORS["show"], 0, 2),
            ("🥈 PLACE", MODERN_COLORS["place"], 2, 2),
            ("🥇 WIN", MODERN_COLORS["win"], 4, 3)
        ]

        for text, color_config, col, span in headers:
            header = tk.Label(parent, text=text, font=("Segoe UI", 15, "bold"),
                              bg=color_config["bg"], fg=color_config["fg"],
                              relief="flat", bd=0, height=2)
            header.grid(row=0, column=col, columnspan=span, sticky="ew", padx=3, pady=3)

            # Racing-themed border with shadow effect
            header.configure(highlightthickness=1, highlightbackground=color_config["shadow"])

    def _setup_betting_buttons(self, parent):
        """Set up the betting buttons with racing silk theme - better scaling."""
        for horse_idx, horse in enumerate(HORSES):
            row = horse_idx + 1

            # Better sized racing silk-themed horse label
            horse_colors = MODERN_COLORS["horse_silks"].get(horse, {"bg": "#6b7280", "accent": "#9ca3af"})
            horse_label = tk.Label(parent, text=f"🐎 {horse}", font=("Segoe UI", 11, "bold"),
                                   bg=horse_colors["bg"], fg="white",
                                   width=9, height=2, relief="flat", bd=0)
            horse_label.grid(row=row, column=7, padx=3, pady=3, sticky="ew")
            horse_label.configure(highlightthickness=1, highlightbackground=horse_colors["accent"])

            # Better sized betting spots with enhanced racing theme
            horse_bets = BETTING_GRID[horse_idx]
            self.bet_buttons[horse] = {}

            for col_idx, (multiplier, penalty) in enumerate(horse_bets):
                bet_type = "show" if col_idx < 2 else "place" if col_idx < 4 else "win"
                color_config = MODERN_COLORS[bet_type]

                # Clearer button text with better formatting
                if penalty > 0:
                    btn_text = f"{multiplier}x\n-${penalty}"
                else:
                    btn_text = f"{multiplier}x\nFREE"

                btn = tk.Button(parent, text=btn_text, font=("Segoe UI", 10, "bold"),
                                bg=color_config["bg"], fg=color_config["fg"],
                                activebackground=color_config["hover"], activeforeground=color_config["fg"],
                                relief="flat", bd=0, width=7, height=2, cursor="hand2",
                                command=lambda h=horse, t=bet_type, m=multiplier, p=penalty, r=row, c=col_idx:
                                self.on_standard_bet(h, t, m, p, r, c))
                btn.grid(row=row, column=col_idx, padx=3, pady=3, sticky="ew")

                # Subtle racing-themed border
                btn.configure(highlightthickness=1, highlightbackground=color_config["shadow"])

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
        """Set up the current bets display with racing theme."""
        # Racing-themed card container
        bets_container = tk.Frame(parent, bg=MODERN_COLORS["card"], relief="flat", bd=0)
        bets_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        bets_container.configure(highlightthickness=2, highlightbackground=MODERN_COLORS["accent"])

        # Racing-themed title
        title_frame = tk.Frame(bets_container, bg=MODERN_COLORS["card"])
        title_frame.pack(fill="x", pady=(20, 15))

        title_label = tk.Label(title_frame, text=f"{TRACK_PATTERNS['trophy']} ACTIVE BETS",
                               font=("Segoe UI", 16, "bold"),
                               bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_primary"])
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Track all placed wagers",
                                  font=("Segoe UI", 9, "italic"),
                                  bg=MODERN_COLORS["card"], fg=MODERN_COLORS["text_secondary"])
        subtitle_label.pack(pady=(2, 0))

        # Treeview container with racing styling
        tree_frame = tk.Frame(bets_container, bg=MODERN_COLORS["surface"])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 15))
        tree_frame.configure(highlightthickness=1, highlightbackground=MODERN_COLORS["border"])

        # Enhanced racing-themed Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Racing.Treeview",
                        background=MODERN_COLORS["surface"],
                        foreground=MODERN_COLORS["text_primary"],
                        fieldbackground=MODERN_COLORS["surface"],
                        borderwidth=0,
                        relief="flat",
                        rowheight=25)
        style.configure("Racing.Treeview.Heading",
                        background=MODERN_COLORS["track"],
                        foreground="white",
                        borderwidth=0,
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))

        self.bets_tree = ttk.Treeview(tree_frame,
                                      columns=("Player", "Horse", "Type", "Token", "Win", "Lose", "Remove"),
                                      show="headings", height=18, style="Racing.Treeview")

        # Configure columns with racing theme
        columns = [
            ("Player", 90), ("Horse", 70), ("Type", 90), ("Token", 70),
            ("Win", 70), ("Lose", 70), ("Remove", 80)
        ]

        for col, width in columns:
            self.bets_tree.heading(col, text=f"🏇 {col}" if col == "Player" else
            f"🐎 {col}" if col == "Horse" else
            f"💰 {col}" if col in ["Win", "Token"] else
            f"💸 {col}" if col == "Lose" else
            f"🗑️ {col}" if col == "Remove" else col)
            self.bets_tree.column(col, width=width)

        # Racing-themed scrollbar
        bets_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.bets_tree.yview)
        self.bets_tree.configure(yscrollcommand=bets_scrollbar.set)

        self.bets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        bets_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)

        # Racing-themed action buttons
        button_frame = tk.Frame(bets_container, bg=MODERN_COLORS["card"])
        button_frame.pack(pady=(10, 20), fill="x", padx=20)

        self.remove_btn = tk.Button(button_frame, text=f"{TRACK_PATTERNS['horse']} Remove Selected Bet",
                                    font=("Segoe UI", 11, "bold"),
                                    bg=MODERN_COLORS["danger"], fg="white",
                                    activebackground="#b91c1c", activeforeground="white",
                                    relief="flat", bd=0, height=2, cursor="hand2")
        self.remove_btn.pack(side=tk.TOP, pady=(0, 8), fill="x")
        self.remove_btn.configure(highlightthickness=2, highlightbackground="#7f1d1d")

        self.clear_btn = tk.Button(button_frame, text=f"{TRACK_PATTERNS['checkered']} Clear All Bets",
                                   font=("Segoe UI", 11, "bold"),
                                   bg=MODERN_COLORS["secondary"], fg="white",
                                   activebackground="#334155", activeforeground="white",
                                   relief="flat", bd=0, height=2, cursor="hand2")
        self.clear_btn.pack(side=tk.TOP, fill="x")
        self.clear_btn.configure(highlightthickness=2, highlightbackground="#1e293b")

    def update_button_appearance(self, horse: str, bet_type: str, row: int, col: int, player: str):
        """Update button appearance to show it's locked."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]

                    new_text = f"{multiplier}x\n{player[:7]}"
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
                new_text = f"{lines[0]}\n{lines[1]}\n🏇 {player[:8]}"
            else:
                new_text = f"{current_text}\n🏇 {player[:8]}"

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
                new_text = f"{lines[0]}\n{lines[1]}\n🏇 {player[:8]}"
            else:
                new_text = f"{current_text}\n🏇 {player[:8]}"

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

            # Keep the first 4 lines (name, description, multiplier, "Up to 3 jockeys")
            if len(lines) >= 4:
                player_text = ", ".join([f"🏇 {p[:6]}" for p in players])
                new_text = f"{lines[0]}\n{lines[1]}\n{lines[2]}\n{player_text}"
            else:
                player_text = ", ".join([f"🏇 {p[:6]}" for p in players])
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
                    if penalty > 0:
                        btn_text = f"{multiplier}x\n-${penalty}"
                    else:
                        btn_text = f"{multiplier}x\nFREE"

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
                        btn_text = f"🏇 {name}\n{TRACK_PATTERNS['trophy']} {payout} Payout\n💸 (-$1 risk)"
                    else:
                        btn_text = f"🐎 {name}\n{TRACK_PATTERNS['trophy']} {payout} Payout\n{TRACK_PATTERNS['checkered']} No Risk!"

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
            btn_text = f"{prop_bet['description']}\n{prop_bet['multiplier']}x | -${prop_bet['penalty']}"

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
            btn_text = f"{TRACK_PATTERNS['trophy']} {exotic_finish['name']}\n{exotic_finish['description']}\n💰 {exotic_finish['multiplier']}x (-${exotic_finish['penalty']})\n🏇 Up to 3 jockeys"

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
        """Update the bets display - compact version."""
        # Clear existing items
        for item in self.bets_tree.get_children():
            self.bets_tree.delete(item)

        # Add current bets - no Remove column for space
        for bet in bets.values():
            penalty_text = f"-${bet.potential_loss}" if bet.potential_loss > 0 else "FREE"

            # Determine bet type display - more compact
            if bet.is_prop_bet():
                horse_display = "🔮Prop"
                type_display = f"#{bet.prop_bet_id}"
            elif bet.is_exotic_bet():
                horse_display = "✨Exotic"
                type_display = f"#{bet.exotic_finish_id}"
            else:
                horse_display = bet.horse if bet.horse != "Special" else "🌟Special"
                type_display = bet.bet_type[:8] + "..." if len(bet.bet_type) > 8 else bet.bet_type

            self.bets_tree.insert("", tk.END, values=(
                bet.player[:8],  # Truncate long names
                horse_display,
                type_display,
                f"${bet.token_value}",
                f"+${bet.potential_payout}",
                penalty_text
            ))