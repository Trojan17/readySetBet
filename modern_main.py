"""
Ready Set Bet - Modern Betting Application
Entry point for the CustomTkinter version
"""

import customtkinter as ctk
from src.modern_app import ModernReadySetBetApp

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

def main():
    """Main entry point for the modern application."""
    root = ctk.CTk()
    app = ModernReadySetBetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()