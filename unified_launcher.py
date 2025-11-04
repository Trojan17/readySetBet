"""
ALL-IN-ONE Launcher for Ready Set Bet
This is the ONLY .exe you need!
"""
import customtkinter as ctk
import subprocess
import sys
import os
import threading
import time
from tkinter import messagebox

class UnifiedLauncher(ctk.CTk):
    """Single unified launcher - does EVERYTHING"""

    def __init__(self):
        super().__init__()

        self.title("🎰 Ready Set Bet")
        self.geometry("600x700")  # Increased height to show all content
        self.resizable(True, True)  # Allow resizing

        # Server process
        self.server_process = None
        self.server_running = False

        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI"""
        # Scrollable container to ensure all content is visible
        scrollable = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable.pack(fill="both", expand=True, padx=40, pady=40)

        # Main container
        container = ctk.CTkFrame(scrollable, fg_color="transparent")
        container.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            container,
            text="🎰 Ready Set Bet",
            font=("Arial", 36, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            container,
            text="Multiplayer Horse Betting Game",
            font=("Arial", 16)
        )
        subtitle.pack(pady=(0, 40))

        # Instructions
        instructions = ctk.CTkLabel(
            container,
            text="Choose how you want to play:",
            font=("Arial", 14)
        )
        instructions.pack(pady=(0, 30))

        # HOST button
        host_frame = ctk.CTkFrame(container, fg_color="#1a4d2e", corner_radius=15)
        host_frame.pack(fill="x", pady=(0, 20))

        host_label = ctk.CTkLabel(
            host_frame,
            text="🖥️  Host a Game",
            font=("Arial", 18, "bold")
        )
        host_label.pack(pady=(20, 5))

        host_desc = ctk.CTkLabel(
            host_frame,
            text="Start a new game on your computer.\nFriends can connect to play with you.",
            font=("Arial", 13),
            text_color="lightgray",
            justify="center"
        )
        host_desc.pack(pady=(0, 15))

        host_btn = ctk.CTkButton(
            host_frame,
            text="🚀 Host a Game",
            command=self.host_game,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        host_btn.pack(fill="x", padx=30, pady=(0, 20))

        # JOIN button
        join_frame = ctk.CTkFrame(container, fg_color="#1a3a4d", corner_radius=15)
        join_frame.pack(fill="x", pady=(0, 20))

        join_label = ctk.CTkLabel(
            join_frame,
            text="🎮  Join a Friend's Game",
            font=("Arial", 18, "bold")
        )
        join_label.pack(pady=(20, 5))

        join_desc = ctk.CTkLabel(
            join_frame,
            text="Connect to a friend's game.\nThey'll give you the address and code.",
            font=("Arial", 13),
            text_color="lightgray",
            justify="center"
        )
        join_desc.pack(pady=(0, 15))

        join_btn = ctk.CTkButton(
            join_frame,
            text="🚀 Join a Game",
            command=self.join_game,
            height=50,
            font=("Arial", 16, "bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        join_btn.pack(fill="x", padx=30, pady=(0, 20))

    def host_game(self):
        """Host a game - starts server automatically"""
        # Hide this window
        self.withdraw()

        # Show progress window
        progress = ctk.CTkToplevel(self)
        progress.title("Starting Server...")
        progress.geometry("500x300")
        progress.transient(self)
        progress.grab_set()

        status_label = ctk.CTkLabel(
            progress,
            text="🔄 Starting server...\nPlease wait...",
            font=("Arial", 14)
        )
        status_label.pack(expand=True, pady=20)

        def start_server_and_game():
            try:
                # Check dependencies
                try:
                    import uvicorn
                    import fastapi
                except ImportError:
                    self.after(0, lambda: messagebox.showerror(
                        "Missing Dependencies",
                        "Server dependencies not installed!\n\n"
                        "Run: pip install -r server/requirements.txt"
                    ))
                    self.after(0, progress.destroy)
                    self.after(0, self.deiconify)
                    return

                # Start server in background
                python_exe = sys.executable
                if sys.platform == "win32":
                    self.server_process = subprocess.Popen(
                        [python_exe, "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"],
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                else:
                    self.server_process = subprocess.Popen(
                        [python_exe, "-m", "uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )

                self.server_running = True

                # Update status
                self.after(0, lambda: status_label.configure(
                    text="✅ Server started!\n🔄 Getting your IP address..."
                ))

                # Wait a moment for server to start
                time.sleep(3)

                # Get public IP
                try:
                    import requests
                    public_ip = requests.get('https://api.ipify.org', timeout=5).text
                    ip_text = f"ws://{public_ip}:8000"
                except:
                    ip_text = "ws://YOUR_IP:8000"

                # Update status
                self.after(0, lambda: status_label.configure(
                    text=f"✅ Server running!\n🔄 Launching game..."
                ))

                time.sleep(1)

                # Close progress and launch game
                self.after(0, progress.destroy)
                self.after(0, lambda: self._launch_game_as_host(ip_text))

            except Exception as e:
                self.after(0, lambda: messagebox.showerror(
                    "Error",
                    f"Failed to start server:\n{str(e)}"
                ))
                self.after(0, progress.destroy)
                self.after(0, self.deiconify)

        # Start in thread
        threading.Thread(target=start_server_and_game, daemon=True).start()

    def _launch_game_as_host(self, server_ip):
        """Launch the game as host"""
        # Set environment to indicate we're hosting
        os.environ["READYSETBET_MODE"] = "host"
        os.environ["READYSETBET_SERVER"] = "ws://localhost:8000"
        os.environ["READYSETBET_SERVER_PUBLIC_IP"] = server_ip

        # Hide launcher
        self.destroy()

        # Import and launch multiplayer game directly (works in .exe)
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from src.multiplayer_app import MultiplayerReadySetBetApp

        # Create new root window
        root = ctk.CTk()

        # Create app - it will detect host mode from env vars
        app = MultiplayerReadySetBetApp(root)

        # Run main loop
        root.mainloop()

    def join_game(self):
        """Join a game - shows connection dialog"""
        # Hide this window
        self.withdraw()

        # Show join dialog
        from src.simple_join_dialog import SimpleJoinDialog

        dialog = SimpleJoinDialog(self)
        result = dialog.get_result()

        if not result:
            # User cancelled
            self.deiconify()
            return

        player_name, server_url, session_id = result

        # Set environment
        os.environ["READYSETBET_MODE"] = "join"
        os.environ["READYSETBET_SERVER"] = server_url
        os.environ["READYSETBET_PLAYER_NAME"] = player_name
        os.environ["READYSETBET_SESSION_ID"] = session_id

        # Destroy launcher
        self.destroy()

        # Import and launch multiplayer game directly (works in .exe)
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
        from src.multiplayer_app import MultiplayerReadySetBetApp

        # Create new root window
        root = ctk.CTk()

        # Create app - it will detect join mode from env vars
        app = MultiplayerReadySetBetApp(root)

        # Run main loop
        root.mainloop()


def main():
    """Main entry point"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = UnifiedLauncher()
    app.mainloop()


if __name__ == "__main__":
    main()
