#!/usr/bin/env python3
"""
Ready Set Bet - Multiplayer Game Client (For Friends)
This is what friends use to JOIN your game
"""
import customtkinter as ctk
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.simple_join_dialog import SimpleJoinDialog
from src.network_client import NetworkClient
from src.multiplayer_app import MultiplayerReadySetBetApp


class SimpleMultiplayerClient:
    """Simple join-only multiplayer client"""

    def __init__(self, root):
        self.root = root

        # Show simple join dialog
        dialog = SimpleJoinDialog(root)
        result = dialog.get_result()

        if not result:
            # User cancelled
            root.quit()
            return

        player_name, server_url, session_id = result

        # Initialize network client
        self.network_client = NetworkClient(server_url)

        # Join the session
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Show connecting message
        status_window = ctk.CTkToplevel(root)
        status_window.title("Connecting...")
        status_window.geometry("400x150")
        status_label = ctk.CTkLabel(
            status_window,
            text=f"Connecting to {server_url}...",
            font=("Arial", 14)
        )
        status_label.pack(expand=True)
        status_window.update()

        # Try to join
        success = self.network_client.join_session(session_id, player_name)

        if not success:
            status_window.destroy()
            error_window = ctk.CTkToplevel(root)
            error_window.title("Connection Failed")
            error_window.geometry("400x200")

            error_label = ctk.CTkLabel(
                error_window,
                text="❌ Failed to join session!\n\n"
                     "Possible reasons:\n"
                     "• Wrong server address\n"
                     "• Wrong session code\n"
                     "• Session is full (max 9 players)\n"
                     "• Name already taken",
                font=("Arial", 12),
                justify="left"
            )
            error_label.pack(expand=True, padx=20, pady=20)

            close_btn = ctk.CTkButton(
                error_window,
                text="Close",
                command=lambda: [error_window.destroy(), root.quit()]
            )
            close_btn.pack(pady=10)

            return

        status_window.destroy()

        # Connected! Now start the game
        # We need to start the actual game with the network client
        self._start_game(player_name, server_url, session_id)

    def _start_game(self, player_name, server_url, session_id):
        """Start the actual game"""
        # Import and setup game
        from src.modern_app import ModernReadySetBetApp
        from src.multiplayer_app import MultiplayerReadySetBetApp

        # Create game instance (will connect via network client)
        # For now, just create the multiplayer app manually
        # This is a workaround - the multiplayer app expects the lobby dialog

        # Show success message
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Connected!")
        success_window.geometry("400x150")

        success_label = ctk.CTkLabel(
            success_window,
            text=f"✅ Connected to session {session_id}!\n\n"
                 f"Starting game...",
            font=("Arial", 14)
        )
        success_label.pack(expand=True)

        # Close after 2 seconds and launch game
        self.root.after(2000, success_window.destroy)
        self.root.after(2000, lambda: self._launch_game(player_name, server_url, session_id))

    def _launch_game(self, player_name, server_url, session_id):
        """Launch the actual game window"""
        # This is complex because MultiplayerReadySetBetApp expects to show lobby dialog
        # For now, just show a message
        msg_window = ctk.CTkToplevel(self.root)
        msg_window.title("Game Starting")
        msg_window.geometry("400x150")

        msg_label = ctk.CTkLabel(
            msg_window,
            text="Game is starting!\n\n"
                 f"Player: {player_name}\n"
                 f"Server: {server_url}\n"
                 f"Session: {session_id}",
            font=("Arial", 12)
        )
        msg_label.pack(expand=True)


def main():
    """Main entry point"""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.withdraw()  # Hide main window

    app = SimpleMultiplayerClient(root)

    root.mainloop()


if __name__ == "__main__":
    main()
