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
        self.geometry("600x750")

        # Center window
        self.transient(parent)
        self.grab_set()

        # Result values
        self.result: Optional[Tuple[str, str, str, str]] = None  # (mode, session_id, player_name, server_url)

        self._setup_ui()

        # Wait for window
        self.wait_window()

    def _setup_ui(self):
        """Setup the lobby UI"""
        # Scrollable container
        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            scrollable,
            text="🎰 Ready Set Bet Multiplayer",
            font=("Arial", 26, "bold")
        )
        title.pack(pady=(0, 10))

        # Player name (always needed)
        name_label = ctk.CTkLabel(scrollable, text="Your Name:", font=("Arial", 14, "bold"))
        name_label.pack(anchor="w", pady=(10, 5))

        self.name_var = ctk.StringVar()
        self.name_entry = ctk.CTkEntry(
            scrollable,
            textvariable=self.name_var,
            placeholder_text="Enter your display name",
            height=40,
            font=("Arial", 13)
        )
        self.name_entry.pack(fill="x", pady=(0, 20))
        self.name_entry.focus()

        # Separator
        separator1 = ctk.CTkFrame(scrollable, height=3, fg_color="gray")
        separator1.pack(fill="x", pady=20)

        # CREATE SECTION (for host)
        create_frame = ctk.CTkFrame(scrollable, fg_color="#1a4d2e", corner_radius=10)
        create_frame.pack(fill="x", pady=(0, 10))

        create_label = ctk.CTkLabel(
            create_frame,
            text="🖥️  HOST A GAME",
            font=("Arial", 16, "bold")
        )
        create_label.pack(pady=(15, 5))

        create_hint = ctk.CTkLabel(
            create_frame,
            text="Use this if the server is running on THIS computer\n(You clicked 'Start Server' in the launcher)",
            font=("Arial", 12),
            text_color="lightgray",
            justify="center"
        )
        create_hint.pack(pady=(0, 15))

        create_btn = ctk.CTkButton(
            create_frame,
            text="🎲 Create New Session",
            command=self._create_session,
            height=50,
            font=("Arial", 15, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        create_btn.pack(fill="x", padx=20, pady=(0, 20))

        # Separator
        separator2 = ctk.CTkFrame(scrollable, height=3, fg_color="gray")
        separator2.pack(fill="x", pady=20)

        # JOIN SECTION (for friends)
        join_frame = ctk.CTkFrame(scrollable, fg_color="#1a3a4d", corner_radius=10)
        join_frame.pack(fill="x", pady=(0, 10))

        join_label = ctk.CTkLabel(
            join_frame,
            text="🎮  JOIN A FRIEND'S GAME",
            font=("Arial", 16, "bold")
        )
        join_label.pack(pady=(15, 5))

        join_hint = ctk.CTkLabel(
            join_frame,
            text="Use this to connect to a friend's server\n(They will give you the address and code)",
            font=("Arial", 12),
            text_color="lightgray",
            justify="center"
        )
        join_hint.pack(pady=(0, 15))

        # Server URL for joining
        server_label = ctk.CTkLabel(join_frame, text="Server Address:", font=("Arial", 13, "bold"))
        server_label.pack(anchor="w", padx=20, pady=(10, 5))

        self.server_url_var = ctk.StringVar(value="ws://")
        self.server_entry = ctk.CTkEntry(
            join_frame,
            textvariable=self.server_url_var,
            placeholder_text="ws://73.45.123.89:8000",
            height=40,
            font=("Arial", 13)
        )
        self.server_entry.pack(fill="x", padx=20, pady=(0, 5))

        server_example = ctk.CTkLabel(
            join_frame,
            text="Example: ws://73.45.123.89:8000",
            font=("Arial", 10),
            text_color="gray"
        )
        server_example.pack(anchor="w", padx=20, pady=(0, 15))

        # Session code for joining
        session_label = ctk.CTkLabel(join_frame, text="Session Code:", font=("Arial", 13, "bold"))
        session_label.pack(anchor="w", padx=20, pady=(0, 5))

        self.session_var = ctk.StringVar()
        self.session_entry = ctk.CTkEntry(
            join_frame,
            textvariable=self.session_var,
            placeholder_text="8-character code",
            height=40,
            font=("Arial", 13)
        )
        self.session_entry.pack(fill="x", padx=20, pady=(0, 5))

        session_example = ctk.CTkLabel(
            join_frame,
            text="Example: ABC123XY",
            font=("Arial", 10),
            text_color="gray"
        )
        session_example.pack(anchor="w", padx=20, pady=(0, 15))

        # Join button
        join_btn = ctk.CTkButton(
            join_frame,
            text="🚀 Join Session",
            command=self._join_session,
            height=50,
            font=("Arial", 15, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        join_btn.pack(fill="x", padx=20, pady=(0, 20))

        # Status label
        self.status_label = ctk.CTkLabel(
            scrollable,
            text="",
            font=("Arial", 12),
            text_color="red",
            wraplength=550
        )
        self.status_label.pack(pady=(15, 0))

    def _create_session(self):
        """Handle create session button"""
        player_name = self.name_var.get().strip()

        if not player_name:
            self.status_label.configure(text="❌ Please enter your name at the top")
            return

        if len(player_name) > 50:
            self.status_label.configure(text="❌ Name too long (max 50 characters)")
            return

        # Create on localhost
        self.result = ("create", "", player_name, "ws://localhost:8000")
        self.destroy()

    def _join_session(self):
        """Handle join session button"""
        player_name = self.name_var.get().strip()
        server_url = self.server_url_var.get().strip()
        session_id = self.session_var.get().strip().upper()

        # Validate
        if not player_name:
            self.status_label.configure(text="❌ Please enter your name at the top")
            return

        if len(player_name) > 50:
            self.status_label.configure(text="❌ Name too long (max 50 characters)")
            return

        if not server_url or server_url == "ws://":
            self.status_label.configure(text="❌ Please enter the server address")
            return

        if not server_url.startswith("ws://") and not server_url.startswith("wss://"):
            self.status_label.configure(text="❌ Server address must start with ws:// or wss://")
            return

        if not session_id:
            self.status_label.configure(text="❌ Please enter the session code")
            return

        if len(session_id) != 8:
            self.status_label.configure(text="❌ Session code must be exactly 8 characters")
            return

        self.result = ("join", session_id, player_name, server_url)
        self.destroy()

    def get_result(self) -> Optional[Tuple[str, str, str, str]]:
        """Get the dialog result"""
        return self.result
