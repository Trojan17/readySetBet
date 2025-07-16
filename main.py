"""
Ready Set Bet - Betting Application
A digital betting board for the Ready Set Bet horse racing game.
"""

import tkinter as tk
from src.app import ReadySetBetApp

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    ReadySetBetApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
