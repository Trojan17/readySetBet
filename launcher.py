"""
Simple Launcher GUI for Ready Set Bet
Choose to start server or play multiplayer
"""
import customtkinter as ctk
import subprocess
import sys
import os
import threading

class LauncherGUI(ctk.CTk):
    """Main launcher window"""

    def __init__(self):
        super().__init__()

        self.title("🎰 Ready Set Bet Launcher")
        self.geometry("600x700")
        self.resizable(True, True)

        # Server process
        self.server_process = None
        self.server_running = False

        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI"""
        # Create scrollable frame
        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=20, pady=20)

        # Main container
        container = ctk.CTkFrame(scrollable, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        title = ctk.CTkLabel(
            container,
            text="🎰 Ready Set Bet",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            container,
            text="Multiplayer Horse Betting Game",
            font=("Arial", 16)
        )
        subtitle.pack(pady=(0, 30))

        # Server section
        server_frame = ctk.CTkFrame(container)
        server_frame.pack(fill="x", pady=(0, 20))

        server_title = ctk.CTkLabel(
            server_frame,
            text="🖥️ Host a Game (Start Server)",
            font=("Arial", 18, "bold")
        )
        server_title.pack(pady=(15, 10))

        server_desc = ctk.CTkLabel(
            server_frame,
            text="Start the server on your computer.\nFriends can connect to play together!",
            font=("Arial", 12),
            justify="center"
        )
        server_desc.pack(pady=(0, 10))

        self.server_btn = ctk.CTkButton(
            server_frame,
            text="🚀 Start Server",
            command=self.start_server,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.server_btn.pack(pady=(0, 10), padx=20, fill="x")

        self.server_status = ctk.CTkLabel(
            server_frame,
            text="",
            font=("Arial", 11),
            text_color="gray"
        )
        self.server_status.pack(pady=(0, 15))

        # Separator
        separator = ctk.CTkFrame(container, height=2)
        separator.pack(fill="x", pady=15)

        # Client section
        client_frame = ctk.CTkFrame(container)
        client_frame.pack(fill="x", pady=(0, 20))

        client_title = ctk.CTkLabel(
            client_frame,
            text="🎮 Join a Game (Play Multiplayer)",
            font=("Arial", 18, "bold")
        )
        client_title.pack(pady=(15, 10))

        client_desc = ctk.CTkLabel(
            client_frame,
            text="Connect to a server and play!\nYou can play on your own server or join a friend's.",
            font=("Arial", 12),
            justify="center"
        )
        client_desc.pack(pady=(0, 10))

        self.play_btn = ctk.CTkButton(
            client_frame,
            text="🎲 Play Multiplayer",
            command=self.start_client,
            height=45,
            font=("Arial", 14, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.play_btn.pack(pady=(0, 15), padx=20, fill="x")

        # Single player option
        single_frame = ctk.CTkFrame(container)
        single_frame.pack(fill="x")

        single_title = ctk.CTkLabel(
            single_frame,
            text="🏠 Single Player (Local Game)",
            font=("Arial", 18, "bold")
        )
        single_title.pack(pady=(15, 10))

        single_desc = ctk.CTkLabel(
            single_frame,
            text="Play alone on this computer (no internet needed)",
            font=("Arial", 12)
        )
        single_desc.pack(pady=(0, 10))

        single_btn = ctk.CTkButton(
            single_frame,
            text="🎯 Play Single Player",
            command=self.start_single_player,
            height=40,
            font=("Arial", 13),
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        single_btn.pack(pady=(0, 15), padx=20, fill="x")

    def start_server(self):
        """Start the server"""
        if self.server_running:
            self.server_status.configure(
                text="⚠️ Server is already running!",
                text_color="orange"
            )
            return

        # Check if dependencies are installed
        try:
            import uvicorn
            import fastapi
        except ImportError as e:
            self.server_status.configure(
                text=f"❌ Missing dependencies! Run: pip install -r server/requirements.txt",
                text_color="red"
            )
            return

        self.server_btn.configure(state="disabled", text="Starting...")
        self.server_status.configure(text="🔄 Starting server...", text_color="blue")

        # Get public IP first
        try:
            import requests
            public_ip = requests.get('https://api.ipify.org', timeout=3).text
            ip_text = f"ws://{public_ip}:8000"
        except:
            ip_text = "ws://YOUR_IP:8000"

        # Start server as subprocess
        try:
            python_exe = sys.executable

            # Try to start server using start_server.py
            if os.path.exists("start_server.py"):
                # On Windows, create new console window
                if sys.platform == "win32":
                    self.server_process = subprocess.Popen(
                        [python_exe, "start_server.py"],
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    self.server_process = subprocess.Popen(
                        [python_exe, "start_server.py"]
                    )
            else:
                # Fallback: run uvicorn directly
                if sys.platform == "win32":
                    self.server_process = subprocess.Popen(
                        [python_exe, "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"],
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    self.server_process = subprocess.Popen(
                        [python_exe, "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
                    )

            self.server_running = True
            self.server_status.configure(
                text=f"✅ Server running! Share: {ip_text}",
                text_color="green"
            )
            self.server_btn.configure(text="✅ Server Running", state="disabled")

        except Exception as e:
            self.server_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color="red"
            )
            self.server_btn.configure(state="normal", text="🚀 Start Server")
            self.server_running = False

    def start_client(self):
        """Start multiplayer client"""
        # Launch multiplayer client
        python_exe = sys.executable
        subprocess.Popen([python_exe, "multiplayer_main.py"])

    def start_single_player(self):
        """Start single player game"""
        # Launch single player
        python_exe = sys.executable
        subprocess.Popen([python_exe, "modern_main.py"])


def main():
    """Main entry point"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = LauncherGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
