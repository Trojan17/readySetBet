# README.md
"""
# Ready Set Bet - Digital Betting Board

A Python application that recreates the betting mechanics of the Ready Set Bet board game.

## Features

- **Authentic Betting System**: Exact multipliers and penalties from the real game
- **Token Management**: 5 tokens per player per round (1×$5, 2×$3, 1×$2, 1×$1)
- **Bet Locking**: Only one player can bet on each spot
- **Visual Feedback**: Color-coded betting board (Gold/Silver/Copper for Win/Place/Show)
- **Special Bets**: Blue Wins, Orange Wins, Red Wins, 7 Finishes 5th or Worse
- **Real-time Updates**: Live bet tracking and player status
- **Penalty System**: Accurate loss penalties for unsuccessful bets

## Installation

1. Ensure Python 3.7+ is installed
2. Clone/download the project files
3. No additional dependencies required (uses tkinter from standard library)

## Usage

```bash
python main.py
```

## Project Structure

```
ready_set_bet/
├── main.py              # Application entry point
├── src/
│   ├── __init__.py      # Package initialization
│   ├── app.py           # Main application class
│   ├── models.py        # Data models (Player, Bet, GameState)
│   ├── game_logic.py    # Game rules and business logic
│   ├── ui_components.py # UI components (BettingBoard)
│   ├── dialogs.py       # Dialog windows
│   └── constants.py     # Game configuration and constants
├── requirements.txt     # Dependencies (none required)
└── README.md           # This file
```

## Game Rules

### Betting
- Each player starts with $0
- Players get 5 tokens per round: 1×$5, 2×$3, 1×$2, 1×$1
- Only one player can bet on each betting spot
- Bets lock the spot until round ends

### Payouts
- **Winning bets**: Token Value × Multiplier
- **Losing bets**: Fixed penalty amount (not multiplied)
- Money cannot go below $0

### Special Bets
- **Blue Wins** (5x, -$1): Horses 2/3, 4, 10, 11/12
- **Orange Wins** (3x, -$1): Horses 5, 9  
- **Red Wins** (2x, -$1): Horses 6, 8
- **7 Finishes 5th or Worse** (4x, no penalty): Horse 7 not in top 3

## Development

### Architecture
- **MVC Pattern**: Separated models, views, and logic
- **Modular Design**: Each component has single responsibility
- **Type Hints**: Full type annotation for better code clarity
- **Dataclasses**: Modern Python data structures

### Key Classes
- `GameState`: Manages all game data
- `Player`: Individual player data and token management
- `Bet`: Represents a single bet with all metadata
- `GameLogic`: Handles race results and payout calculations
- `BettingBoard`: Main UI component for bet placement
- `ReadySetBetApp`: Main application controller

## Contributing

1. Follow existing code style and patterns
2. Add type hints to all new functions
3. Update tests for any business logic changes
4. Maintain separation of concerns between modules

## License

GPL-3.0 license
"""