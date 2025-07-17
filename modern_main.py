"""
Ready Set Bet - Modern Betting Application
Entry point for the CustomTkinter version
"""

import customtkinter as ctk
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.modern_app import ModernReadySetBetApp
except ImportError:
    # Alternative import method
    from modern_app import ModernReadySetBetApp

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

def main():
    """Main entry point for the modern application."""
    try:
        root = ctk.CTk()
        app = ModernReadySetBetApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()