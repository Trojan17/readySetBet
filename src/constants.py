"""Constants and configuration for the Ready Set Bet application."""

from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

# Icon paths
GAME_ICON = ASSETS_DIR / "icon.png"
GAME_LOGO = ASSETS_DIR / "logo.png"

# Game configuration
MAX_RACES = 4
STARTING_MONEY = 0
MINIMUM_MONEY = 0

# Player tokens configuration
PLAYER_TOKENS = {
    "5": 1,    # One token worth 5
    "3": 2,    # Two tokens worth 3 each
    "2": 1,    # One token worth 2
    "1": 1     # One token worth 1
}

# Horse configuration
HORSES = ["2/3", "4", "5", "6", "7", "8", "9", "10", "11/12"]

# UI Theme Colors - Centralized color management
class Theme:
    # Main colors
    SURFACE = "#111827"
    CARD = "#1f2937"
    PRIMARY = "#1f2937"
    SECONDARY = "#374151"

    # Action colors
    ACCENT = "#3b82f6"
    SUCCESS = "#10b981"
    WARNING = "#f59e0b"
    DANGER = "#ef4444"
    DISABLED = "#6b7280"

    # Betting colors
    SHOW = "#cd7f32"      # Bronze
    PLACE = "#c0c0c0"     # Silver
    WIN = "#ffd700"       # Gold
    LOCKED = "#6b7280"    # Gray

    # Special bet colors
    BLUE_BET = "#2563eb"
    ORANGE_BET = "#ea580c"
    RED_BET = "#dc2626"
    BLACK_BET = "#7c2d12"

    # Other bet types
    PROP = "#7c3aed"      # Purple
    EXOTIC = "#0891b2"    # Teal

    # Text colors
    TEXT_LIGHT = "#ffffff"
    TEXT_DARK = "#000000"
    TEXT_MUTED = "#9ca3af"

# Horse colors for visual reference
HORSE_COLORS = {
    "2/3": Theme.BLUE_BET,
    "4": Theme.BLUE_BET,
    "5": Theme.ORANGE_BET,
    "6": Theme.RED_BET,
    "7": "#000000",
    "8": Theme.RED_BET,
    "9": Theme.ORANGE_BET,
    "10": Theme.BLUE_BET,
    "11/12": Theme.BLUE_BET
}

# Betting grid data - (multiplier, penalty) - 0 means no penalty
BETTING_GRID = [
    # Row 1: Horse 2/3 - Show: 4x(-4), 4x(-3); Place: 5x(-4), 5x(-3); Win: 7x(-2), 8x(-2), 9x(-2)
    [(4, 4), (4, 3), (5, 4), (5, 3), (7, 2), (8, 2), (9, 2)],
    # Row 2: Horse 4 - Show: 3x(-1), 3x(0); Place: 4x(-1), 4x(0); Win: 5x(-1), 6x(0), 7x(0)
    [(3, 1), (3, 0), (4, 1), (4, 0), (5, 1), (6, 0), (7, 0)],
    # Row 3: Horse 5 - Show: 2x(-3), 2x(0); Place: 2x(-2), 3x(-2); Win: 4x(-2), 4x(0), 5x(0)
    [(2, 3), (2, 0), (2, 2), (3, 2), (4, 2), (4, 0), (5, 0)],
    # Row 4: Horse 6 - Show: 1x(-2), 1x(0); Place: 2x(-5), 2x(-4); Win: 3x(-2), 3x(-1), 3x(0)
    [(1, 2), (1, 0), (2, 5), (2, 4), (3, 2), (3, 1), (3, 0)],
    # Row 5: Horse 7 - Show: 1x(-3), 1x(-1); Place: 2x(-6), 2x(-5); Win: 3x(-4), 3x(-3), 3x(-2)
    [(1, 3), (1, 1), (2, 6), (2, 5), (3, 4), (3, 3), (3, 2)],
    # Row 6: Horse 8 - Show: 1x(-2), 1x(0); Place: 2x(-5), 2x(-4); Win: 3x(-2), 3x(-1), 3x(0)
    [(1, 2), (1, 0), (2, 5), (2, 4), (3, 2), (3, 1), (3, 0)],
    # Row 7: Horse 9 - Show: 2x(-3), 2x(0); Place: 2x(-2), 3x(-2); Win: 4x(-2), 4x(0), 5x(0)
    [(2, 3), (2, 0), (2, 2), (3, 2), (4, 2), (4, 0), (5, 0)],
    # Row 8: Horse 10 - Show: 3x(-1), 3x(0); Place: 4x(-1), 4x(0); Win: 5x(-1), 6x(0), 7x(0)
    [(3, 1), (3, 0), (4, 1), (4, 0), (5, 1), (6, 0), (7, 0)],
    # Row 9: Horse 11/12 - Show: 4x(-4), 4x(-3); Place: 5x(-4), 5x(-3); Win: 7x(-2), 8x(-2), 9x(-2)
    [(4, 4), (4, 3), (5, 4), (5, 3), (7, 2), (8, 2), (9, 2)]
]

# Special bets configuration
SPECIAL_BETS = [
    ("Blue Wins", "5x", "blue"),
    ("Orange Wins", "3x", "orange"),
    ("Red Wins", "2x", "red"),
    ("7 Finishes 5th or Worse", "4x", "black")
]

# Prop bets configuration - All available prop bets
PROP_BETS = [
    {"id": 1, "description": " 8 >  5 & 9", "multiplier": 3, "penalty": 3},
    {"id": 2, "description": " 4 >  9", "multiplier": 2, "penalty": 1},
    {"id": 3, "description": " 8 >  2/3, 4, 10, 11/12", "multiplier": 2, "penalty": 3},
    {"id": 4, "description": " 9 >  8", "multiplier": 2, "penalty": 1},
    {"id": 5, "description": " 5 >  8", "multiplier": 3, "penalty": 3},
    {"id": 6, "description": " 4 >  5", "multiplier": 3, "penalty": 3},
    {"id": 7, "description": " 11/12 >  8", "multiplier": 4, "penalty": 3},
    {"id": 8, "description": " 9 >  6", "multiplier": 3, "penalty": 3},
    {"id": 9, "description": " 9 >  7", "multiplier": 4, "penalty": 4},
    {"id": 10, "description": " 7 >  2/3 & 4 & 10 & 11/12", "multiplier": 2, "penalty": 6},
    {"id": 11, "description": " 2/3 >  5", "multiplier": 2, "penalty": 1},
    {"id": 12, "description": " 10 >  8", "multiplier": 3, "penalty": 2},
    {"id": 13, "description": " 11/12 >  9", "multiplier": 3, "penalty": 3},
    {"id": 14, "description": " 2/3 >  8", "multiplier": 4, "penalty": 3},
    {"id": 15, "description": " 4 >  6", "multiplier": 4, "penalty": 3},
    {"id": 16, "description": " 10 >  9", "multiplier": 2, "penalty": 1},
    {"id": 17, "description": " 5 >  6", "multiplier": 2, "penalty": 1},
    {"id": 18, "description": " 11/12 >  6", "multiplier": 3, "penalty": 2},
    {"id": 19, "description": " 11/12 >  5", "multiplier": 2, "penalty": 1},
    {"id": 20, "description": " 4 >  8", "multiplier": 3, "penalty": 2},
    {"id": 21, "description": " 6 >  2/3, 4, 10, 11/12", "multiplier": 3, "penalty": 5},
    {"id": 22, "description": " 5 >  7", "multiplier": 3, "penalty": 2},
    {"id": 23, "description": " 2/3 >  9", "multiplier": 3, "penalty": 3},
    {"id": 24, "description": " 6 >  5, 9", "multiplier": 3, "penalty": 3},
    {"id": 25, "description": " 10 >  5", "multiplier": 3, "penalty": 3},
    {"id": 26, "description": " 2/3 >  6", "multiplier": 3, "penalty": 2},
    {"id": 27, "description": " 10 >  6", "multiplier": 4, "penalty": 3},
    {"id": 28, "description": " 7 >  5 & 9", "multiplier": 2, "penalty": 5}
]

# Exotic Finish bets configuration
EXOTIC_FINISHES = [
    {"id": 1, "name": "BY A NOSE", "description": "The 2nd place horse loses by exactly 1 space", "multiplier": 5, "penalty": 3},
    {"id": 2, "name": "BLOW OUT", "description": "The 2nd place horse loses by more than 5 spaces", "multiplier": 4, "penalty": 2},
    {"id": 3, "name": "TIGHT RACE", "description": "All horses move 6 or more spaces", "multiplier": 6, "penalty": 2},
    {"id": 4, "name": "LATE START", "description": "At least 2 horses move 3 or fewer spaces", "multiplier": 4, "penalty": 1},
    {"id": 5, "name": "PHOTO FINISH", "description": "The 3rd place horse loses by 3 or fewer spaces", "multiplier": 5, "penalty": 3}
]

# UI Colors - Legacy support (keeping for backward compatibility)
COLORS = {
    "show": {
        "bg": Theme.SHOW,
        "fg": "white"
    },
    "place": {
        "bg": Theme.PLACE,
        "fg": "black"
    },
    "win": {
        "bg": Theme.WIN,
        "fg": "black"
    },
    "locked": {
        "bg": Theme.LOCKED,
        "fg": "white"
    },
    "special": {
        "blue": {"bg": Theme.BLUE_BET, "fg": "white"},
        "orange": {"bg": Theme.ORANGE_BET, "fg": "white"},
        "red": {"bg": Theme.RED_BET, "fg": "white"},
        "black": {"bg": Theme.BLACK_BET, "fg": "white"}
    },
    "prop": {
        "bg": Theme.PROP,
        "fg": "white"
    },
    "exotic": {
        "bg": Theme.EXOTIC,
        "fg": "white"
    }
}

# VIP Cards (simplified set)
VIP_CARDS = [
    {"name": "Lucky Seven", "effect": "Win $2 when 7 is rolled", "type": "roll_bonus", "target": 7, "amount": 2},
    {"name": "Snake Eyes", "effect": "Win $3 when 2 is rolled", "type": "roll_bonus", "target": 2, "amount": 3},
    {"name": "Boxcars", "effect": "Win $3 when 12 is rolled", "type": "roll_bonus", "target": 12, "amount": 3},
    {"name": "Favorite", "effect": "Win $1 when your favorite horse wins", "type": "win_bonus", "amount": 1},
    {"name": "Longshot", "effect": "Win $2 when horses 2 or 12 place", "type": "place_bonus", "targets": [2, 12], "amount": 2},
    {"name": "Double Up", "effect": "Next winning bet pays double", "type": "double_next", "amount": 2},
    {"name": "Free Bet", "effect": "Place one bet without paying", "type": "free_bet", "amount": 1},
    {"name": "Insurance", "effect": "Get $1 back on losing bets", "type": "insurance", "amount": 1},
]