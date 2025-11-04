"""
Multiplayer extension for Ready Set Bet
Wraps ModernReadySetBetApp with network functionality
"""
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, Dict
import os

from .modern_app import ModernReadySetBetApp
from .network_client import NetworkClient
from .lobby_dialog import LobbyDialog
from .models import GameState, Player, Bet


class MultiplayerReadySetBetApp(ModernReadySetBetApp):
    """Multiplayer version of Ready Set Bet app"""

    def __init__(self, root):
        # Check if launched from unified launcher
        mode_env = os.getenv("READYSETBET_MODE")

        if mode_env == "host":
            # Auto-host mode from unified launcher
            server_url = os.getenv("READYSETBET_SERVER", "ws://localhost:8000")
            self.server_public_ip = os.getenv("READYSETBET_SERVER_PUBLIC_IP", "ws://YOUR_IP:8000")

            # Ask for player name only
            name_dialog = ctk.CTkInputDialog(
                text="Enter your name:",
                title="Ready Set Bet - Host"
            )
            player_name = name_dialog.get_input()

            if not player_name:
                root.quit()
                return

            mode = "create"
            session_id = ""
            self.is_host_mode = True

        elif mode_env == "join":
            # Auto-join mode from unified launcher
            server_url = os.getenv("READYSETBET_SERVER", "ws://localhost:8000")
            player_name = os.getenv("READYSETBET_PLAYER_NAME", "")
            session_id = os.getenv("READYSETBET_SESSION_ID", "")
            mode = "join"
            self.is_host_mode = False
            self.server_public_ip = None

        else:
            # Normal mode - show lobby dialog
            self.lobby_dialog = LobbyDialog(root)
            lobby_result = self.lobby_dialog.get_result()

            if not lobby_result:
                # User cancelled
                root.quit()
                return

            mode, session_id, player_name, server_url = lobby_result
            self.is_host_mode = False
            self.server_public_ip = None

        # Initialize network client
        self.network_client = NetworkClient(server_url)
        self.my_player_name = player_name
        self.is_connected = False

        # Initialize parent (creates game state and UI)
        super().__init__(root)

        # Override window title
        self.root.title(f"🏇 Ready Set Bet - Multiplayer ({player_name})")

        # Add connection status indicator
        self._setup_connection_indicator()

        # Disable Add Player button in multiplayer mode
        if "add_player" in self.control_buttons:
            self.control_buttons["add_player"].configure(state="disabled")

        # Setup network callbacks
        self._setup_network_callbacks()

        # Create or join session
        if mode == "create":
            self._create_and_join_session()
        else:
            self._join_existing_session(session_id)

    def _setup_connection_indicator(self):
        """Add connection status indicator to status bar"""
        # Create a frame in the status bar
        status_frame = self.root.grid_slaves(row=2, column=0)[0]

        self.connection_label = ctk.CTkLabel(
            status_frame,
            text="⚪ Connecting...",
            font=ctk.CTkFont(size=12),
            anchor="e"
        )
        self.connection_label.pack(side="right", padx=15, pady=10)

    def _update_connection_status(self, connected: bool):
        """Update connection status indicator"""
        if connected:
            self.connection_label.configure(
                text=f"🟢 Connected to {self.network_client.session_id}",
                text_color="green"
            )
            self.is_connected = True
        else:
            self.connection_label.configure(
                text="🔴 Disconnected",
                text_color="red"
            )
            self.is_connected = False

    def _setup_network_callbacks(self):
        """Register callbacks for network messages"""
        self.network_client.register_callback("connected", self._on_connected)
        self.network_client.register_callback("disconnected", self._on_disconnected)
        self.network_client.register_callback("state_sync", self._on_state_sync)
        self.network_client.register_callback("player_connected", self._on_player_event)
        self.network_client.register_callback("player_disconnected", self._on_player_event)
        self.network_client.register_callback("race_started", self._on_race_started)
        self.network_client.register_callback("race_ended", self._on_race_ended)
        self.network_client.register_callback("game_completed", self._on_game_completed)
        self.network_client.register_callback("error", self._on_error)

    def _create_and_join_session(self):
        """Create a new session and join it"""
        self.status_var.set("Creating new session...")

        session_id = self.network_client.create_session()
        if not session_id:
            messagebox.showerror("Error", "Failed to create session. Check server connection.")
            self.root.quit()
            return

        # Join the session
        success = self.network_client.join_session(session_id, self.my_player_name)
        if not success:
            messagebox.showerror("Error", "Failed to join session.")
            self.root.quit()
            return

        # Start WebSocket connection
        self.network_client.start_connection()

        self.status_var.set(f"✅ Session {session_id} created! Share this code with friends.")

        # If in host mode from unified launcher, show session info popup
        if self.is_host_mode and self.server_public_ip:
            # Delay to ensure main window is fully rendered first
            self.root.after(500, lambda: self._show_session_info(session_id, self.server_public_ip))

    def _show_session_info(self, session_id: str, server_ip: str):
        """Show session information to host"""
        info_window = ctk.CTkToplevel(self.root)
        info_window.title("Game Created!")
        info_window.geometry("550x400")
        info_window.transient(self.root)
        # Don't use grab_set() - allows clicking on game board while popup is visible
        info_window.attributes("-topmost", True)  # Keep popup visible but not blocking

        # Container
        container = ctk.CTkFrame(info_window, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Title
        title = ctk.CTkLabel(
            container,
            text="✅ Game Created Successfully!",
            font=("Arial", 22, "bold"),
            text_color="green"
        )
        title.pack(pady=(0, 20))

        # Instructions
        instructions = ctk.CTkLabel(
            container,
            text="Share this information with your friends:",
            font=("Arial", 14)
        )
        instructions.pack(pady=(0, 20))

        # Server address box
        server_frame = ctk.CTkFrame(container, fg_color="#2d2d2d")
        server_frame.pack(fill="x", pady=(0, 15))

        server_label = ctk.CTkLabel(
            server_frame,
            text="Server Address:",
            font=("Arial", 13, "bold")
        )
        server_label.pack(anchor="w", padx=15, pady=(15, 5))

        server_entry = ctk.CTkEntry(
            server_frame,
            width=450,
            height=40,
            font=("Arial", 14),
            justify="center"
        )
        server_entry.insert(0, server_ip)
        server_entry.configure(state="readonly")
        server_entry.pack(padx=15, pady=(0, 15))

        # Session code box
        code_frame = ctk.CTkFrame(container, fg_color="#2d2d2d")
        code_frame.pack(fill="x", pady=(0, 20))

        code_label = ctk.CTkLabel(
            code_frame,
            text="Session Code:",
            font=("Arial", 13, "bold")
        )
        code_label.pack(anchor="w", padx=15, pady=(15, 5))

        code_entry = ctk.CTkEntry(
            code_frame,
            width=450,
            height=40,
            font=("Arial", 18, "bold"),
            justify="center"
        )
        code_entry.insert(0, session_id)
        code_entry.configure(state="readonly")
        code_entry.pack(padx=15, pady=(0, 15))

        # Instructions
        hint = ctk.CTkLabel(
            container,
            text="Friends need both the server address AND session code to join!",
            font=("Arial", 12),
            text_color="yellow"
        )
        hint.pack(pady=(0, 10))

        # Note about non-blocking
        note = ctk.CTkLabel(
            container,
            text="You can start playing! This window won't block the game.",
            font=("Arial", 11),
            text_color="lightgray"
        )
        note.pack(pady=(0, 20))

        # Close button
        close_btn = ctk.CTkButton(
            container,
            text="Close (or keep open for reference)",
            command=info_window.destroy,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        close_btn.pack(fill="x")

    def _join_existing_session(self, session_id: str):
        """Join an existing session"""
        self.status_var.set(f"Joining session {session_id}...")

        success = self.network_client.join_session(session_id, self.my_player_name)
        if not success:
            messagebox.showerror("Error", f"Failed to join session {session_id}. Session may be full or not found.")
            self.root.quit()
            return

        # Start WebSocket connection
        self.network_client.start_connection()

        self.status_var.set(f"✅ Joined session {session_id}")

    def _on_connected(self):
        """Called when WebSocket connects"""
        self._update_connection_status(True)
        # Request initial state
        self.network_client.request_state()

    def _on_disconnected(self):
        """Called when WebSocket disconnects"""
        self._update_connection_status(False)
        self.status_var.set("⚠️ Connection lost. Attempting to reconnect...")

    def _on_state_sync(self, message: dict):
        """Called when server sends full state update"""
        state_data = message["data"]

        # Update game state from server
        self._apply_server_state(state_data)

        # Update UI
        self._update_displays()
        self._update_button_states()
        self.betting_board.refresh_all_buttons()

    def _apply_server_state(self, state_data: dict):
        """Apply server state to local game state"""
        # Update race info
        self.game_state.current_race = state_data["current_race"]
        self.game_state.max_races = state_data["max_races"]
        self.game_state.race_active = state_data["race_active"]
        self.game_state.status = state_data["status"]

        # Update players
        self.game_state.players.clear()
        for player_data in state_data["players"]:
            player = Player(
                name=player_data["name"],
                money=player_data["money"],
                vip_cards=player_data["vip_cards"],
                tokens=player_data["tokens"],
                used_tokens=player_data["used_tokens"]
            )
            self.game_state.players[player.name] = player

        # Update bets
        self.game_state.current_bets.clear()
        for bet_data in state_data["current_bets"]:
            bet = Bet(
                player=bet_data["player"],
                horse=bet_data["horse"],
                bet_type=bet_data["bet_type"],
                multiplier=bet_data["multiplier"],
                penalty=bet_data["penalty"],
                token_value=bet_data["token_value"],
                spot_key=bet_data["spot_key"],
                row=bet_data.get("row"),
                col=bet_data.get("col"),
                prop_bet_id=bet_data.get("prop_bet_id"),
                exotic_finish_id=bet_data.get("exotic_finish_id")
            )
            self.game_state.current_bets[bet.spot_key] = bet

        # Update locked spots
        self.game_state.locked_spots = state_data["locked_spots"]

        # Update prop bets and exotic finishes
        self.game_state.current_prop_bets = state_data["current_prop_bets"]
        self.game_state.current_exotic_finishes = state_data["current_exotic_finishes"]

        # Update betting board
        self.betting_board.update_prop_bets(self.game_state.current_prop_bets)
        self.betting_board.update_exotic_finishes(self.game_state.current_exotic_finishes)
        self.betting_board.set_betting_enabled(self.game_state.race_active)

        # Update race label
        self.race_label.configure(text=f"Race: {self.game_state.current_race}/{self.game_state.max_races}")

    def _on_player_event(self, message: dict):
        """Called when a player connects or disconnects"""
        # State sync will be sent by server, just show notification
        player_name = message.get("player_name", "Unknown")
        if message["type"] == "player_connected":
            self.status_var.set(f"👋 {player_name} joined the game")
        else:
            self.status_var.set(f"👋 {player_name} left the game")

    def _on_race_started(self, message: dict):
        """Called when race starts"""
        race_number = message.get("race_number", self.game_state.current_race)
        self.status_var.set(f"🚦 Race {race_number} started! Place your bets.")

    def _on_race_ended(self, message: dict):
        """Called when race ends"""
        self.status_var.set("🏁 Race ended! Waiting for next race...")

    def _on_game_completed(self, message: dict):
        """Called when game is complete"""
        self.status_var.set("🎉 Game completed! Final standings displayed.")
        messagebox.showinfo("Game Complete", "The game has ended. Check final standings!")

    def _on_error(self, message: dict):
        """Called when server sends error"""
        error_msg = message.get("message", "Unknown error")
        messagebox.showerror("Server Error", error_msg)

    # Override betting methods to send to server
    def on_standard_bet(self, horse: str, bet_type: str, multiplier: int, penalty: int, row: int, col: int):
        """Override to send bet to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        if not self._validate_betting():
            return

        spot_key = f"{horse}_{bet_type}_{row}_{col}"
        if spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error", f"This betting spot is already taken by {self.game_state.locked_spots[spot_key]}!")
            return

        # Only allow player to bet for themselves
        from .modern_dialogs import ModernStandardBetDialog

        # Create modified dialog that only shows current player
        my_player = {self.my_player_name: self.game_state.players.get(self.my_player_name)}
        dialog = ModernStandardBetDialog(self.root, my_player, horse, bet_type, multiplier, penalty)
        result = dialog.show()

        if result:
            # Send bet to server
            bet_data = {
                "horse": horse,
                "bet_type": bet_type,
                "multiplier": multiplier,
                "penalty": penalty,
                "token_value": result["token_value"],
                "spot_key": spot_key,
                "row": row,
                "col": col
            }
            self.network_client.place_bet(bet_data)

    def on_special_bet(self, bet_name: str, multiplier: int):
        """Override to send special bet to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        if not self._validate_betting():
            return

        spot_key = f"special_{bet_name}"
        if spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error", f"This special bet is already taken by {self.game_state.locked_spots[spot_key]}!")
            return

        from .modern_dialogs import ModernSpecialBetDialog

        my_player = {self.my_player_name: self.game_state.players.get(self.my_player_name)}
        dialog = ModernSpecialBetDialog(self.root, my_player, bet_name, multiplier)
        result = dialog.show()

        if result:
            bet_data = {
                "horse": "Special",
                "bet_type": bet_name,
                "multiplier": multiplier,
                "penalty": 1,
                "token_value": result["token_value"],
                "spot_key": spot_key
            }
            self.network_client.place_bet(bet_data)

    def on_prop_bet(self, prop_bet: dict):
        """Override to send prop bet to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        if not self._validate_betting():
            return

        spot_key = f"prop_{prop_bet['id']}"
        if spot_key in self.game_state.locked_spots:
            messagebox.showerror("Error", f"This prop bet is already taken by {self.game_state.locked_spots[spot_key]}!")
            return

        from .modern_dialogs import ModernPropBetDialog

        my_player = {self.my_player_name: self.game_state.players.get(self.my_player_name)}
        dialog = ModernPropBetDialog(self.root, my_player, prop_bet)
        result = dialog.show()

        if result:
            bet_data = {
                "horse": "Prop",
                "bet_type": "prop",
                "multiplier": prop_bet["multiplier"],
                "penalty": prop_bet["penalty"],
                "token_value": result["token_value"],
                "spot_key": spot_key,
                "prop_bet_id": prop_bet["id"]
            }
            self.network_client.place_bet(bet_data)

    def on_exotic_bet(self, exotic_finish: dict):
        """Override to send exotic bet to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        if not self._validate_betting():
            return

        spot_key = f"exotic_{exotic_finish['id']}"

        # Exotic finishes allow multiple bets (max 3)
        exotic_bet_count = sum(1 for bet in self.game_state.current_bets.values()
                               if bet.exotic_finish_id == exotic_finish['id'])
        if exotic_bet_count >= 3:
            messagebox.showerror("Error", "This exotic finish already has 3 bets (maximum reached)!")
            return

        from .modern_dialogs import ModernExoticFinishDialog

        my_player = {self.my_player_name: self.game_state.players.get(self.my_player_name)}
        dialog = ModernExoticFinishDialog(self.root, my_player, exotic_finish)
        result = dialog.show()

        if result:
            # Create unique spot key for this player's exotic bet
            player_spot_key = f"{spot_key}_{self.my_player_name}"

            bet_data = {
                "horse": "Exotic",
                "bet_type": "exotic",
                "multiplier": exotic_finish["multiplier"],
                "penalty": exotic_finish["penalty"],
                "token_value": result["token_value"],
                "spot_key": player_spot_key,
                "exotic_finish_id": exotic_finish["id"]
            }
            self.network_client.place_bet(bet_data)

    # Override control methods to send to server
    def start_race(self):
        """Override to send start_race to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        self.network_client.start_race()

    def end_race(self):
        """Override to send end_race to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        # Show race results dialog
        from .modern_dialogs import ModernRaceResultsDialog
        dialog = ModernRaceResultsDialog(self.root, self.game_state)
        results = dialog.show()

        if results:
            # Send results to server
            self.network_client.end_race(results)

    def next_race(self):
        """Override to send next_race to server"""
        if not self.is_connected:
            messagebox.showerror("Error", "Not connected to server")
            return

        self.network_client.next_race()

    def reset_game(self):
        """Disable reset in multiplayer mode"""
        messagebox.showinfo("Multiplayer Mode", "Game reset is not available in multiplayer mode. Start a new session instead.")

    def add_player(self):
        """Disable add player in multiplayer mode"""
        messagebox.showinfo("Multiplayer Mode", "Players join via the lobby. You cannot add players manually.")
