"""Constants and configuration for the Ready Set Bet application."""

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

# Horse colors for visual reference
HORSE_COLORS = {
    "2/3": "#4A90E2",    # Blue
    "4": "#4A90E2",      # Blue
    "5": "#F5A623",      # Orange
    "6": "#D0021B",      # Red
    "7": "#000000",      # Black
    "8": "#D0021B",      # Red
    "9": "#F5A623",      # Orange
    "10": "#4A90E2",     # Blue
    "11/12": "#4A90E2"   # Blue
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
    {"id": 1, "description": "Horse 8 > Horses 5 & 9", "multiplier": 3, "penalty": 3},
    {"id": 2, "description": "Horse 4 > Horse 9", "multiplier": 2, "penalty": 1},
    {"id": 3, "description": "Horse 8 > Horses 2/3, 4, 10, 11/12", "multiplier": 2, "penalty": 3},
    {"id": 4, "description": "Horse 9 > Horse 8", "multiplier": 2, "penalty": 1},
    {"id": 5, "description": "Horse 5 > Horse 8", "multiplier": 3, "penalty": 3},
    {"id": 6, "description": "Horse 4 > Horse 5", "multiplier": 3, "penalty": 3},
    {"id": 7, "description": "Horse 11/12 > Horse 8", "multiplier": 4, "penalty": 3},
    {"id": 8, "description": "Horse 9 > Horse 6", "multiplier": 3, "penalty": 3},
    {"id": 9, "description": "Horse 9 > Horse 7", "multiplier": 4, "penalty": 4},
    {"id": 10, "description": "Horse 7 > Horses 2/3 & 4 & 10 & 11/12", "multiplier": 2, "penalty": 6},
    {"id": 11, "description": "Horse 2/3 > Horse 5", "multiplier": 2, "penalty": 1},
    {"id": 12, "description": "Horse 10 > Horse 8", "multiplier": 3, "penalty": 2},
    {"id": 13, "description": "Horse 11/12 > Horse 9", "multiplier": 3, "penalty": 3},
    {"id": 14, "description": "Horse 2/3 > Horse 8", "multiplier": 4, "penalty": 3},
    {"id": 15, "description": "Horse 4 > Horse 6", "multiplier": 4, "penalty": 3},
    {"id": 16, "description": "Horse 10 > Horse 9", "multiplier": 2, "penalty": 1},
    {"id": 17, "description": "Horse 5 > Horse 6", "multiplier": 2, "penalty": 1},
    {"id": 18, "description": "Horse 11/12 > Horse 6", "multiplier": 3, "penalty": 2},
    {"id": 19, "description": "Horse 11/12 > Horse 5", "multiplier": 2, "penalty": 1},
    {"id": 20, "description": "Horse 4 > Horse 8", "multiplier": 3, "penalty": 2},
    {"id": 21, "description": "Horse 6 > Horses 2/3, 4, 10, 11/12", "multiplier": 3, "penalty": 5},
    {"id": 22, "description": "Horse 5 > Horse 7", "multiplier": 3, "penalty": 2},
    {"id": 23, "description": "Horse 2/3 > Horse 9", "multiplier": 3, "penalty": 3},
    {"id": 24, "description": "Horse 6 > Horse 5, 9", "multiplier": 3, "penalty": 3},
    {"id": 25, "description": "Horse 10 > Horse 5", "multiplier": 3, "penalty": 3},
    {"id": 26, "description": "Horse 2/3 > Horse 6", "multiplier": 3, "penalty": 2},
    {"id": 27, "description": "Horse 10 > Horse 6", "multiplier": 4, "penalty": 3},
    {"id": 28, "description": "Horse 7 > Horse 5 & 9", "multiplier": 2, "penalty": 5}
]

# Exotic Finish bets configuration
EXOTIC_FINISHES = [
    {"id": 1, "name": "BY A NOSE", "description": "The 2nd place horse loses by exactly 1 space", "multiplier": 5, "penalty": 3},
    {"id": 2, "name": "BLOW OUT", "description": "The 2nd place horse loses by more than 5 spaces", "multiplier": 4, "penalty": 2},
    {"id": 3, "name": "TIGHT RACE", "description": "All horses move 6 or more spaces", "multiplier": 6, "penalty": 2},
    {"id": 4, "name": "LATE START", "description": "At least 2 horses move 3 or fewer spaces", "multiplier": 4, "penalty": 1},
    {"id": 5, "name": "PHOTO FINISH", "description": "The 3rd place horse loses by 3 or fewer spaces", "multiplier": 5, "penalty": 3}
]

# UI Colors
COLORS = {
    "show": {
        "bg": "#B87333",  # Copper
        "fg": "white"
    },
    "place": {
        "bg": "#C0C0C0",  # Silver
        "fg": "black"
    },
    "win": {
        "bg": "#FFD700",  # Gold
        "fg": "black"
    },
    "locked": {
        "bg": "#808080",  # Gray
        "fg": "white"
    },
    "special": {
        "blue": {"bg": "#1976D2", "fg": "white"},
        "orange": {"bg": "#F57C00", "fg": "white"},
        "red": {"bg": "#D32F2F", "fg": "white"},
        "black": {"bg": "#424242", "fg": "white"}
    },
    "prop": {
        "bg": "#7B1FA2",  # Purple
        "fg": "white"
    },
    "exotic": {
        "bg": "#E65100",  # Deep Orange
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