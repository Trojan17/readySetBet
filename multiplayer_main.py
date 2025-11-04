#!/usr/bin/env python3
"""
Ready Set Bet - Multiplayer Main Entry Point
Launch this to play Ready Set Bet in multiplayer mode
"""
import customtkinter as ctk
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.multiplayer_app import MultiplayerReadySetBetApp


def main():
    """Main entry point for multiplayer version"""
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create root window
    root = ctk.CTk()

    # Create app (will show lobby dialog first)
    app = MultiplayerReadySetBetApp(root)

    # Run main loop
    root.mainloop()


if __name__ == "__main__":
    main()
