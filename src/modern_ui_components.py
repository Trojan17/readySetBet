"""Modern UI components for the Ready Set Bet application using CustomTkinter."""

import customtkinter as ctk
from typing import Dict, List, Callable
from .constants import Theme, HORSES, BETTING_GRID, SPECIAL_BETS, HORSE_COLORS


class BettingSection:
    """Base class for betting sections."""

    def __init__(self, parent, title: str, color: str):
        self.parent = parent
        self.buttons = {}
        self.container = self._create_container(title, color)

    def _create_container(self, title: str, color: str):
        """Create the section container."""
        container = ctk.CTkFrame(self.parent, fg_color=Theme.CARD)

        title_label = ctk.CTkLabel(
            container,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=color
        )
        title_label.pack(pady=(15, 10))

        return container

    def pack(self, **kwargs):
        """Pack the container."""
        self.container.pack(**kwargs)

    def set_enabled(self, enabled: bool):
        """Enable/disable all buttons in this section."""
        for button in self._get_all_buttons():
            self._set_button_enabled(button, enabled)

    def _get_all_buttons(self):
        """Get all buttons in this section."""
        buttons = []
        for button in self.buttons.values():
            if isinstance(button, dict):
                buttons.extend(button.values())
            elif isinstance(button, list):
                buttons.extend(button)
            else:
                buttons.append(button)
        return buttons

    def _set_button_enabled(self, button, enabled: bool):
        """Set individual button enabled state."""
        if hasattr(button, 'configure'):
            current_color = button.cget("fg_color")
            if current_color != Theme.LOCKED:
                button.configure(state="normal" if enabled else "disabled")


class PropBetsSection(BettingSection):
    """Proposition bets section."""

    def __init__(self, parent, on_prop_bet: Callable):
        super().__init__(parent, "🎯 PROPOSITION BETS", Theme.PROP)
        self.on_prop_bet = on_prop_bet
        self.buttons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

    def update_bets(self, prop_bets: List[Dict]):
        """Update the displayed prop bets."""
        # Clear existing buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        if not prop_bets:
            ctk.CTkLabel(
                self.buttons_frame,
                text="No proposition bets available",
                text_color=Theme.TEXT_MUTED
            ).pack(pady=20)
            return

        # Configure grid
        for i in range(len(prop_bets)):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Create buttons
        for i, prop_bet in enumerate(prop_bets):
            btn_text = f"{prop_bet['description']}\n💰 {prop_bet['multiplier']}x | 💸 -${prop_bet['penalty']}"

            btn = ctk.CTkButton(
                self.buttons_frame,
                text=btn_text,
                font=ctk.CTkFont(size=15, weight="bold"),
                fg_color=Theme.PROP,
                hover_color="#6d28d9",
                height=90,
                command=lambda pb=prop_bet: self.on_prop_bet(pb)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.buttons[prop_bet["id"]] = btn

    def update_button_appearance(self, prop_id: int, player: str):
        """Update button to show it's taken by player."""
        if prop_id in self.buttons:
            button = self.buttons[prop_id]
            current_text = button.cget("text")
            lines = current_text.split('\n')

            new_text = f"{lines[0]}\n{lines[1]}\n🏇 {player[:8]}"
            button.configure(
                text=new_text,
                fg_color=Theme.LOCKED,
                state="disabled"
            )

    def reset_button(self, prop_id: int, prop_bet: Dict):
        """Reset button to original appearance."""
        if prop_id in self.buttons:
            button = self.buttons[prop_id]
            btn_text = f"{prop_bet['description']}\n💰 {prop_bet['multiplier']}x | 💸 -${prop_bet['penalty']}"

            button.configure(
                text=btn_text,
                fg_color=Theme.PROP,
                state="normal"
            )


class SpecialBetsSection(BettingSection):
    """Special bets section."""

    def __init__(self, parent, on_special_bet: Callable):
        super().__init__(parent, "👑 SPECIAL RACING BETS", Theme.WARNING)
        self.on_special_bet = on_special_bet
        self._create_buttons()

    def _create_buttons(self):
        """Create special bet buttons."""
        buttons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Configure grid
        for i in range(4):
            buttons_frame.grid_columnconfigure(i, weight=1)

        color_map = {
            "blue": Theme.BLUE_BET,
            "orange": Theme.ORANGE_BET,
            "red": Theme.RED_BET,
            "black": Theme.BLACK_BET
        }

        for i, (name, payout, color) in enumerate(SPECIAL_BETS):
            penalty_text = "✅ FREE" if name == "7 Finishes 5th or Worse" else "💸 -$1"
            btn_text = f"{name}\n🏆 {payout} | {penalty_text}"

            multiplier = int(payout.replace('x', ''))

            btn = ctk.CTkButton(
                buttons_frame,
                text=btn_text,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=color_map[color],
                height=70,
                command=lambda n=name, m=multiplier: self.on_special_bet(n, m)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.buttons[name] = btn

    def update_button_appearance(self, bet_name: str, player: str):
        """Update button to show it's taken by player."""
        if bet_name in self.buttons:
            button = self.buttons[bet_name]
            current_text = button.cget("text")

            new_text = f"{current_text}\n🏇 {player[:8]}"
            button.configure(
                text=new_text,
                fg_color=Theme.LOCKED,
                state="disabled"
            )

    def reset_button(self, bet_name: str):
        """Reset button to original appearance."""
        if bet_name in self.buttons:
            button = self.buttons[bet_name]

            # Find original bet info
            for name, payout, color in SPECIAL_BETS:
                if name == bet_name:
                    penalty_text = "✅ FREE" if name == "7 Finishes 5th or Worse" else "💸 -$1"
                    btn_text = f"{name}\n🏆 {payout} | {penalty_text}"

                    color_map = {
                        "blue": Theme.BLUE_BET,
                        "orange": Theme.ORANGE_BET,
                        "red": Theme.RED_BET,
                        "black": Theme.BLACK_BET
                    }

                    button.configure(
                        text=btn_text,
                        fg_color=color_map[color],
                        state="normal"
                    )
                    break


class ExoticFinishesSection(BettingSection):
    """Exotic finishes section."""

    def __init__(self, parent, on_exotic_bet: Callable):
        super().__init__(parent, "⭐ EXOTIC FINISH BETS", Theme.EXOTIC)
        self.on_exotic_bet = on_exotic_bet
        self.buttons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.buttons_frame.pack(fill="x", padx=15, pady=(0, 15))

    def update_bets(self, exotic_finishes: List[Dict]):
        """Update the displayed exotic finishes."""
        # Clear existing buttons
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()

        if not exotic_finishes:
            ctk.CTkLabel(
                self.buttons_frame,
                text="No exotic finish bets available",
                text_color=Theme.TEXT_MUTED
            ).pack(pady=20)
            return

        # Configure grid
        for i in range(len(exotic_finishes)):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Create buttons
        for i, exotic_finish in enumerate(exotic_finishes):
            btn_text = f"{exotic_finish['name']}\n{exotic_finish['description']}\n{exotic_finish['multiplier']}x | -${exotic_finish['penalty']}\nMax 3 players"

            btn = ctk.CTkButton(
                self.buttons_frame,
                text=btn_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                fg_color=Theme.EXOTIC,
                hover_color="#0e7490",
                height=130,
                command=lambda ef=exotic_finish: self.on_exotic_bet(ef)
            )
            btn.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            self.buttons[exotic_finish["id"]] = btn

    def update_button_appearance(self, exotic_id: int, players: List[str]):
        """Update button to show players betting on it."""
        if exotic_id in self.buttons:
            button = self.buttons[exotic_id]
            current_text = button.cget("text")
            lines = current_text.split('\n')

            # Keep first 3 lines, replace player info
            player_text = ", ".join([f"🏇 {p[:6]}" for p in players])
            new_text = f"{lines[0]}\n{lines[1]}\n{lines[2]}\n{player_text}"

            # Lock if 3 players
            if len(players) >= 3:
                button.configure(
                    text=new_text,
                    fg_color=Theme.LOCKED,
                    state="disabled"
                )
            else:
                button.configure(text=new_text)

    def reset_button(self, exotic_id: int, exotic_finish: Dict):
        """Reset button to original appearance."""
        if exotic_id in self.buttons:
            button = self.buttons[exotic_id]
            btn_text = f"{exotic_finish['name']}\n{exotic_finish['description']}\n{exotic_finish['multiplier']}x | -${exotic_finish['penalty']}\nMax 3 players"

            button.configure(
                text=btn_text,
                fg_color=Theme.EXOTIC,
                state="normal"
            )


class HorseRacingGrid(BettingSection):
    """Main horse racing odds grid."""

    def __init__(self, parent, on_standard_bet: Callable):
        super().__init__(parent, "🏁 RACING ODDS BOARD", Theme.WIN)
        self.on_standard_bet = on_standard_bet
        self.bet_buttons = {}
        self._create_grid()

    def _create_grid(self):
        """Create the main betting grid."""
        grid_frame = ctk.CTkFrame(self.container, fg_color=Theme.SURFACE)
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Configure columns
        for i in range(8):
            grid_frame.grid_columnconfigure(i, weight=1)

        # Headers
        self._create_headers(grid_frame)

        # Betting buttons
        self._create_betting_buttons(grid_frame)

    def _create_headers(self, parent):
        """Create betting grid headers."""
        headers = [
            ("🥉 SHOW", Theme.SHOW, 0, 2),
            ("🥈 PLACE", Theme.PLACE, 2, 2),
            ("🥇 WIN", Theme.WIN, 4, 3)
        ]

        for text, color, col, span in headers:
            header = ctk.CTkLabel(
                parent,
                text=text,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=color,
                text_color=Theme.TEXT_DARK if color == Theme.WIN else Theme.TEXT_LIGHT,
                height=45,
                corner_radius=8
            )
            header.grid(row=0, column=col, columnspan=span, padx=2, pady=2, sticky="ew")

    def _create_betting_buttons(self, parent):
        """Create the betting buttons grid."""
        for horse_idx, horse in enumerate(HORSES):
            row = horse_idx + 1

            # Horse label
            horse_color = HORSE_COLORS.get(horse, Theme.BLUE_BET)
            horse_label = ctk.CTkLabel(
                parent,
                text=f"🐎 {horse}",
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=horse_color,
                text_color="white",
                height=35,
                corner_radius=6
            )
            horse_label.grid(row=row, column=7, padx=2, pady=2, sticky="ew")

            # Initialize button storage
            self.bet_buttons[horse] = {}

            # Create betting buttons
            horse_bets = BETTING_GRID[horse_idx]

            for col_idx, (multiplier, penalty) in enumerate(horse_bets):
                bet_type = "show" if col_idx < 2 else "place" if col_idx < 4 else "win"

                self._create_bet_button(
                    parent, horse, bet_type, multiplier, penalty, row, col_idx
                )

    def _create_bet_button(self, parent, horse: str, bet_type: str,
                          multiplier: int, penalty: int, row: int, col: int):
        """Create a single betting button."""
        color_map = {
            "show": Theme.SHOW,
            "place": Theme.PLACE,
            "win": Theme.WIN
        }

        color = color_map[bet_type]
        text_color = Theme.TEXT_DARK if bet_type == "win" else Theme.TEXT_LIGHT

        btn_text = f"{multiplier}x\n-${penalty}" if penalty > 0 else f"{multiplier}x\nFREE"

        btn = ctk.CTkButton(
            parent,
            text=btn_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=color,
            text_color=text_color,
            height=35,
            corner_radius=6,
            command=lambda: self.on_standard_bet(horse, bet_type, multiplier, penalty, row, col)
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")

        # Store button reference
        if bet_type not in self.bet_buttons[horse]:
            self.bet_buttons[horse][bet_type] = []

        self.bet_buttons[horse][bet_type].append({
            "button": btn,
            "row": row,
            "col": col,
            "multiplier": multiplier,
            "penalty": penalty
        })

    def _get_all_buttons(self):
        """Get all buttons in this section."""
        buttons = []
        for horse_buttons in self.bet_buttons.values():
            for bet_type_buttons in horse_buttons.values():
                for btn_info in bet_type_buttons:
                    buttons.append(btn_info["button"])
        return buttons

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
                        fg_color=Theme.LOCKED,
                        state="disabled"
                    )
                    break

    def reset_button(self, horse: str, bet_type: str, row: int, col: int):
        """Reset button to original appearance."""
        if bet_type in self.bet_buttons[horse]:
            for btn_info in self.bet_buttons[horse][bet_type]:
                if btn_info["row"] == row and btn_info["col"] == col:
                    button = btn_info["button"]
                    multiplier = btn_info["multiplier"]
                    penalty = btn_info["penalty"]

                    color_map = {
                        "show": Theme.SHOW,
                        "place": Theme.PLACE,
                        "win": Theme.WIN
                    }

                    color = color_map[bet_type]
                    text_color = Theme.TEXT_DARK if bet_type == "win" else Theme.TEXT_LIGHT
                    btn_text = f"{multiplier}x\n-${penalty}" if penalty > 0 else f"{multiplier}x\nFREE"

                    button.configure(
                        text=btn_text,
                        fg_color=color,
                        text_color=text_color,
                        state="normal"
                    )
                    break

    def reset_all_buttons(self):
        """Reset all buttons to original appearance."""
        for horse in HORSES:
            for bet_type in ["show", "place", "win"]:
                if bet_type in self.bet_buttons[horse]:
                    for btn_info in self.bet_buttons[horse][bet_type]:
                        self.reset_button(horse, bet_type, btn_info["row"], btn_info["col"])


class ModernBettingBoard:
    """Main betting board component."""

    def __init__(self, parent, on_standard_bet: Callable, on_special_bet: Callable,
                 on_prop_bet: Callable, on_exotic_bet: Callable):
        self.parent = parent
        self.game_state = None
        self.main_app_callback = None

        # Create main container
        self.container = ctk.CTkScrollableFrame(
            parent,
            fg_color=Theme.SURFACE,
            scrollbar_fg_color=Theme.CARD
        )
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Create sections
        self.prop_section = PropBetsSection(self.container, on_prop_bet)
        self.prop_section.pack(pady=(0, 15), fill="x")

        self.special_section = SpecialBetsSection(self.container, on_special_bet)
        self.special_section.pack(pady=(0, 15), fill="x")

        self.exotic_section = ExoticFinishesSection(self.container, on_exotic_bet)
        self.exotic_section.pack(pady=(0, 15), fill="x")

        self.grid_section = HorseRacingGrid(self.container, on_standard_bet)
        self.grid_section.pack(pady=(0, 15), fill="x")

        # Current bets section
        self._create_current_bets_section()

    def _create_current_bets_section(self):
        """Create the current bets display section."""
        bets_container = ctk.CTkFrame(self.container, fg_color=Theme.CARD)
        bets_container.pack(pady=(0, 15), fill="x")

        # Title
        ctk.CTkLabel(
            bets_container,
            text="🎫 ACTIVE BETS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=Theme.SUCCESS
        ).pack(pady=(15, 10))

        # Scrollable frame for bet cards
        self.bets_scroll_frame = ctk.CTkScrollableFrame(
            bets_container,
            fg_color=Theme.SURFACE,
            height=200
        )
        self.bets_scroll_frame.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Clear all button
        self.clear_btn = ctk.CTkButton(
            bets_container,
            text="🧹 Clear All Bets",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=Theme.DISABLED,
            hover_color="#4b5563",
            height=35,
            command=self.clear_all_bets
        )
        self.clear_btn.pack(fill="x", padx=15, pady=(0, 15))

    def set_game_state(self, game_state):
        """Set reference to game state."""
        self.game_state = game_state

    def set_main_app_callback(self, callback):
        """Set callback to update main app when bets change."""
        self.main_app_callback = callback

    def update_prop_bets(self, prop_bets: List[Dict]):
        """Update proposition bets."""
        self.prop_section.update_bets(prop_bets)

    def update_exotic_finishes(self, exotic_finishes: List[Dict]):
        """Update exotic finishes."""
        self.exotic_section.update_bets(exotic_finishes)

    def set_betting_enabled(self, enabled: bool):
        """Enable/disable all betting."""
        self.prop_section.set_enabled(enabled)
        self.special_section.set_enabled(enabled)
        self.exotic_section.set_enabled(enabled)
        self.grid_section.set_enabled(enabled)

    def update_button_appearance(self, horse: str, bet_type: str, row: int, col: int, player: str):
        """Update standard bet button appearance."""
        self.grid_section.update_button_appearance(horse, bet_type, row, col, player)

    def update_special_bet_appearance(self, bet_name: str, player: str):
        """Update special bet button appearance."""
        self.special_section.update_button_appearance(bet_name, player)

    def update_prop_bet_appearance(self, prop_id: int, player: str):
        """Update prop bet button appearance."""
        self.prop_section.update_button_appearance(prop_id, player)

    def update_exotic_finish_appearance(self, exotic_id: int, players: List[str]):
        """Update exotic finish button appearance."""
        self.exotic_section.update_button_appearance(exotic_id, players)

    def reset_all_buttons(self):
        """Reset all buttons to original appearance."""
        self.grid_section.reset_all_buttons()

        # Reset special bets
        for bet_name in self.special_section.buttons.keys():
            self.special_section.reset_button(bet_name)

    def reset_prop_buttons_to_purple(self, prop_bets: List[Dict]):
        """Reset prop bet buttons."""
        for prop_bet in prop_bets:
            self.prop_section.reset_button(prop_bet["id"], prop_bet)

    def reset_exotic_finishes_to_orange(self, exotic_finishes: List[Dict]):
        """Reset exotic finish buttons."""
        for exotic_finish in exotic_finishes:
            self.exotic_section.reset_button(exotic_finish["id"], exotic_finish)

    def update_bets_display(self, bets: Dict):
        """Update the current bets display."""
        # Clear existing bet cards
        for widget in self.bets_scroll_frame.winfo_children():
            widget.destroy()

        if not bets:
            ctk.CTkLabel(
                self.bets_scroll_frame,
                text="No active bets placed.\n\nStart betting to see them here!",
                font=ctk.CTkFont(size=12),
                text_color=Theme.TEXT_MUTED
            ).pack(pady=20)
            return

        # Create bet cards
        for bet_id, bet in bets.items():
            self._create_bet_card(bet_id, bet)

    def _create_bet_card(self, bet_id: str, bet):
        """Create an individual bet card."""
        bet_card = ctk.CTkFrame(self.bets_scroll_frame, fg_color=Theme.CARD)
        bet_card.pack(fill="x", padx=5, pady=3)
        bet_card.grid_columnconfigure(0, weight=1)

        # Bet info
        info_frame = ctk.CTkFrame(bet_card, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=8)
        info_frame.grid_columnconfigure(0, weight=1)

        # Format bet info
        penalty_text = f"-${bet.potential_loss}" if bet.potential_loss > 0 else "FREE"

        if bet.is_prop_bet():
            bet_info = f"🎯 PROP #{bet.prop_bet_id}"
            bet_color = Theme.PROP
        elif bet.is_exotic_bet():
            bet_info = f"⭐ EXOTIC #{bet.exotic_finish_id}"
            bet_color = Theme.EXOTIC
        elif bet.horse == "Special":
            bet_info = f"👑 {bet.bet_type}"
            bet_color = Theme.WARNING
        else:
            bet_info = f"🐎 {bet.horse} {bet.bet_type.upper()}"
            bet_color = getattr(Theme, bet.bet_type.upper(), Theme.ACCENT)

        # Player name
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
            text_color=Theme.TEXT_LIGHT
        )
        details_label.grid(row=1, column=0, sticky="w", pady=(2, 0))

        # Remove button
        remove_btn = ctk.CTkButton(
            bet_card,
            text="🗑️",
            font=ctk.CTkFont(size=14),
            fg_color=Theme.DANGER,
            hover_color="#dc2626",
            width=40,
            height=30,
            command=lambda bid=bet_id: self.remove_specific_bet(bid)
        )
        remove_btn.grid(row=0, column=1, padx=(5, 10), pady=8)

    def remove_specific_bet(self, bet_id: str):
        """Remove a specific bet."""
        if not self.game_state:
            return

        bet = self.game_state.current_bets.get(bet_id)
        if bet and self.game_state.remove_bet(bet_id):
            # Update display
            self.update_bets_display(self.game_state.current_bets)
            # Reset button appearance
            self._reset_bet_button(bet)
            # Update main app
            if self.main_app_callback:
                self.main_app_callback()

    def clear_all_bets(self):
        """Clear all current bets."""
        if not self.game_state:
            return

        self.game_state.clear_all_bets()
        self.reset_all_buttons()
        self.reset_prop_buttons_to_purple(
            self.game_state.current_prop_bets if self.game_state.current_prop_bets else []
        )
        self.reset_exotic_finishes_to_orange(
            self.game_state.current_exotic_finishes if self.game_state.current_exotic_finishes else []
        )
        self.update_bets_display({})

        if self.main_app_callback:
            self.main_app_callback()

    def _reset_bet_button(self, bet):
        """Reset a specific bet button."""
        if bet.is_prop_bet():
            prop_bet = next(
                (p for p in self.game_state.current_prop_bets if p["id"] == bet.prop_bet_id),
                None
            )
            if prop_bet:
                self.prop_section.reset_button(bet.prop_bet_id, prop_bet)

        elif bet.is_exotic_bet():
            exotic_finish = next(
                (ef for ef in self.game_state.current_exotic_finishes if ef["id"] == bet.exotic_finish_id),
                None
            )
            if exotic_finish:
                # Get remaining players
                remaining_players = [
                    b.player for b in self.game_state.current_bets.values()
                    if b.is_exotic_bet() and b.exotic_finish_id == bet.exotic_finish_id and b.player != bet.player
                ]
                if remaining_players:
                    self.exotic_section.update_button_appearance(bet.exotic_finish_id, remaining_players)
                else:
                    self.exotic_section.reset_button(bet.exotic_finish_id, exotic_finish)

        elif bet.is_special_bet():
            self.special_section.reset_button(bet.bet_type)

        else:
            # Standard bet
            if bet.row is not None and bet.col is not None:
                self.grid_section.reset_button(bet.horse, bet.bet_type, bet.row, bet.col)