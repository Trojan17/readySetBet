"""
Lobby dialog for multiplayer session management
"""
import customtkinter as ctk
from typing import Optional, Tuple
import os


class LobbyDialog(ctk.CTkToplevel):
    """Dialog for creating or joining a multiplayer session"""

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Ready Set Bet - Multiplayer Lobby")
        self.geometry("500x400")

        # Center window
        self.transient(parent)
        self.grab_set()

        # Result values
        self.result: Optional[Tuple[str, str, str, str]] = None  # (mode, session_id, player_name, server_url)

        # Server URL (can be changed by user)
        self.server_url_var = ctk.StringVar(value=os.getenv("READYSETBET_SERVER", "ws://localhost:8000"))

        self._setup_ui()

        # Wait for window
        self.wait_window()

    def _setup_ui(self):
        """Setup the lobby UI"""
        # Main container
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            container,
            text="🎰 Ready Set Bet Multiplayer",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(0, 20))

        # Server URL configuration
        server_frame = ctk.CTkFrame(container)
        server_frame.pack(fill="x", pady=(0, 20))

        server_label = ctk.CTkLabel(server_frame, text="Server URL:", font=("Arial", 12))
        server_label.pack(side="left", padx=(10, 5))

        self.server_entry = ctk.CTkEntry(
            server_frame,
            textvariable=self.server_url_var,
            width=300
        )
        self.server_entry.pack(side="left", padx=(0, 10), pady=10)

        # Player name
        name_frame = ctk.CTkFrame(container)
        name_frame.pack(fill="x", pady=(0, 20))

        name_label = ctk.CTkLabel(name_frame, text="Your Name:", font=("Arial", 12))
        name_label.pack(side="left", padx=(10, 5))

        self.name_var = ctk.StringVar()
        self.name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.name_var,
            placeholder_text="Enter your display name",
            width=300
        )
        self.name_entry.pack(side="left", padx=(0, 10), pady=10)
        self.name_entry.focus()

        # Separator
        separator = ctk.CTkFrame(container, height=2)
        separator.pack(fill="x", pady=10)

        # Create session button
        create_btn = ctk.CTkButton(
            container,
            text="🎲 Create New Game Session",
            command=self._create_session,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        create_btn.pack(fill="x", pady=(10, 10))

        # Join session frame
        join_frame = ctk.CTkFrame(container)
        join_frame.pack(fill="x", pady=(10, 0))

        join_label = ctk.CTkLabel(
            join_frame,
            text="Or join an existing session:",
            font=("Arial", 12)
        )
        join_label.pack(pady=(10, 5))

        # Session ID entry
        session_frame = ctk.CTkFrame(join_frame)
        session_frame.pack(pady=(5, 10))

        session_label = ctk.CTkLabel(session_frame, text="Session Code:", font=("Arial", 12))
        session_label.pack(side="left", padx=(10, 5))

        self.session_var = ctk.StringVar()
        self.session_entry = ctk.CTkEntry(
            session_frame,
            textvariable=self.session_var,
            placeholder_text="Enter 8-character code",
            width=200
        )
        self.session_entry.pack(side="left", padx=(0, 10))

        # Join button
        join_btn = ctk.CTkButton(
            join_frame,
            text="🚀 Join Game",
            command=self._join_session,
            height=40,
            font=("Arial", 14, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        join_btn.pack(fill="x", padx=10, pady=(0, 10))

        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=("Arial", 11),
            text_color="yellow"
        )
        self.status_label.pack(pady=(10, 0))

    def _validate_input(self) -> bool:
        """Validate user input"""
        player_name = self.name_var.get().strip()
        if not player_name:
            self.status_label.configure(text="❌ Please enter your name", text_color="red")
            return False

        if len(player_name) > 50:
            self.status_label.configure(text="❌ Name too long (max 50 characters)", text_color="red")
            return False

        server_url = self.server_url_var.get().strip()
        if not server_url:
            self.status_label.configure(text="❌ Please enter server URL", text_color="red")
            return False

        return True

    def _create_session(self):
        """Handle create session button"""
        if not self._validate_input():
            return

        player_name = self.name_var.get().strip()
        server_url = self.server_url_var.get().strip()

        self.result = ("create", "", player_name, server_url)
        self.destroy()

    def _join_session(self):
        """Handle join session button"""
        if not self._validate_input():
            return

        session_id = self.session_var.get().strip().upper()
        if not session_id:
            self.status_label.configure(text="❌ Please enter a session code", text_color="red")
            return

        if len(session_id) != 8:
            self.status_label.configure(text="❌ Session code must be 8 characters", text_color="red")
            return

        player_name = self.name_var.get().strip()
        server_url = self.server_url_var.get().strip()

        self.result = ("join", session_id, player_name, server_url)
        self.destroy()

    def get_result(self) -> Optional[Tuple[str, str, str, str]]:
        """Get the dialog result"""
        return self.result
