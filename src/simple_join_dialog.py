"""
Simple Join Dialog - For friends connecting to your server
"""
import customtkinter as ctk
from typing import Optional, Tuple
import os


class SimpleJoinDialog(ctk.CTkToplevel):
    """Simple dialog for joining a game session"""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ready Set Bet - Join Game")
        self.geometry("500x450")

        # Center window
        self.transient(parent)
        self.grab_set()

        # Result values
        self.result: Optional[Tuple[str, str, str]] = None  # (player_name, server_url, session_id)

        self._setup_ui()

        # Wait for window
        self.wait_window()

    def _setup_ui(self):
        """Setup the UI"""
        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Title
        title = ctk.CTkLabel(
            container,
            text="🎮 Join a Game",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            container,
            text="Connect to your friend's server",
            font=("Arial", 14)
        )
        subtitle.pack(pady=(0, 30))

        # Player name
        name_label = ctk.CTkLabel(
            container,
            text="Your Name:",
            font=("Arial", 14, "bold")
        )
        name_label.pack(anchor="w", pady=(0, 5))

        self.name_var = ctk.StringVar()
        self.name_entry = ctk.CTkEntry(
            container,
            textvariable=self.name_var,
            placeholder_text="Enter your name (e.g., Bob)",
            height=40,
            font=("Arial", 13)
        )
        self.name_entry.pack(fill="x", pady=(0, 20))
        self.name_entry.focus()

        # Server URL
        server_label = ctk.CTkLabel(
            container,
            text="Server Address:",
            font=("Arial", 14, "bold")
        )
        server_label.pack(anchor="w", pady=(0, 5))

        self.server_var = ctk.StringVar(value="ws://")
        self.server_entry = ctk.CTkEntry(
            container,
            textvariable=self.server_var,
            placeholder_text="ws://73.45.123.89:8000",
            height=40,
            font=("Arial", 13)
        )
        self.server_entry.pack(fill="x", pady=(0, 5))

        server_hint = ctk.CTkLabel(
            container,
            text="(Get this from your friend who is hosting)",
            font=("Arial", 11),
            text_color="gray"
        )
        server_hint.pack(anchor="w", pady=(0, 20))

        # Session code
        session_label = ctk.CTkLabel(
            container,
            text="Session Code:",
            font=("Arial", 14, "bold")
        )
        session_label.pack(anchor="w", pady=(0, 5))

        self.session_var = ctk.StringVar()
        self.session_entry = ctk.CTkEntry(
            container,
            textvariable=self.session_var,
            placeholder_text="Enter 8-character code (e.g., ABC123XY)",
            height=40,
            font=("Arial", 13)
        )
        self.session_entry.pack(fill="x", pady=(0, 5))

        session_hint = ctk.CTkLabel(
            container,
            text="(Also get this from your friend)",
            font=("Arial", 11),
            text_color="gray"
        )
        session_hint.pack(anchor="w", pady=(0, 30))

        # Join button
        join_btn = ctk.CTkButton(
            container,
            text="🚀 Join Game",
            command=self._join,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        join_btn.pack(fill="x")

        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=("Arial", 11),
            text_color="red"
        )
        self.status_label.pack(pady=(10, 0))

    def _join(self):
        """Handle join button"""
        player_name = self.name_var.get().strip()
        server_url = self.server_var.get().strip()
        session_id = self.session_var.get().strip().upper()

        # Validate
        if not player_name:
            self.status_label.configure(text="❌ Please enter your name")
            return

        if not server_url or server_url == "ws://":
            self.status_label.configure(text="❌ Please enter server address")
            return

        if not server_url.startswith("ws://") and not server_url.startswith("wss://"):
            self.status_label.configure(text="❌ Server address must start with ws:// or wss://")
            return

        if not session_id:
            self.status_label.configure(text="❌ Please enter session code")
            return

        if len(session_id) != 8:
            self.status_label.configure(text="❌ Session code must be 8 characters")
            return

        self.result = (player_name, server_url, session_id)
        self.destroy()

    def get_result(self) -> Optional[Tuple[str, str, str]]:
        """Get the dialog result"""
        return self.result
