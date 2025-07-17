"""
Ready Set Bet - Modern Betting Application
Entry point for the CustomTkinter version with icon support
"""

import customtkinter as ctk
from src.modern_app import ModernReadySetBetApp
from src.icon_utils import icon_manager

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

def main():
    """Main entry point for the modern application."""
    root = ctk.CTk()

    # Set the window icon
    icon_manager.set_window_icon(root)

    # Initialize the app
    app = ModernReadySetBetApp(root)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()