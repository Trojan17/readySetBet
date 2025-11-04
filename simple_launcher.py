"""
Simple Server Launcher - ONLY starts the server
"""
import customtkinter as ctk
import subprocess
import sys
import os


class SimpleServerLauncher(ctk.CTk):
    """Simple launcher - ONLY for starting server"""

    def __init__(self):
        super().__init__()

        self.title("🎰 Ready Set Bet - Server")
        self.geometry("550x350")
        self.resizable(False, False)

        # Server process
        self.server_process = None
        self.server_running = False

        self._setup_ui()

    def _setup_ui(self):
        """Setup the UI"""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)

        # Title
        title = ctk.CTkLabel(
            container,
            text="🎰 Ready Set Bet Server",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            container,
            text="Host a multiplayer game on your computer",
            font=("Arial", 14)
        )
        subtitle.pack(pady=(0, 30))

        # Instructions
        instructions = ctk.CTkLabel(
            container,
            text="1. Click 'Start Server' below\n"
                 "2. Share the address shown with friends\n"
                 "3. Run 'ReadySetBet-Game.exe' to play\n"
                 "4. Friends run 'ReadySetBet-Game.exe' to join",
            font=("Arial", 12),
            justify="left"
        )
        instructions.pack(pady=(0, 30))

        # Start server button
        self.server_btn = ctk.CTkButton(
            container,
            text="🚀 Start Server",
            command=self.start_server,
            height=60,
            font=("Arial", 18, "bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.server_btn.pack(fill="x", pady=(0, 15))

        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=("Arial", 12),
            wraplength=450
        )
        self.status_label.pack(pady=(0, 10))

    def start_server(self):
        """Start the server"""
        if self.server_running:
            self.status_label.configure(
                text="⚠️ Server is already running!",
                text_color="orange"
            )
            return

        # Check dependencies
        try:
            import uvicorn
            import fastapi
        except ImportError:
            self.status_label.configure(
                text="❌ Missing dependencies!\nRun: pip install -r server/requirements.txt",
                text_color="red"
            )
            return

        self.server_btn.configure(state="disabled", text="Starting...")
        self.status_label.configure(text="🔄 Starting server...", text_color="blue")

        # Get public IP
        try:
            import requests
            public_ip = requests.get('https://api.ipify.org', timeout=3).text
            ip_text = f"ws://{public_ip}:8000"
        except:
            ip_text = "ws://YOUR_IP:8000"

        # Start server
        try:
            python_exe = sys.executable

            # Start server in new console window
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
            self.status_label.configure(
                text=f"✅ Server running!\n\nShare with friends: {ip_text}\n\n"
                     f"Now run 'ReadySetBet-Game.exe' to play!",
                text_color="green"
            )
            self.server_btn.configure(text="✅ Server Running", fg_color="gray")

        except Exception as e:
            self.status_label.configure(
                text=f"❌ Error: {str(e)}",
                text_color="red"
            )
            self.server_btn.configure(state="normal", text="🚀 Start Server")
            self.server_running = False


def main():
    """Main entry point"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = SimpleServerLauncher()
    app.mainloop()


if __name__ == "__main__":
    main()
