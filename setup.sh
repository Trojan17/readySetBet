#!/bin/bash
echo "============================================================"
echo "Ready Set Bet - Quick Setup"
echo "============================================================"
echo ""
echo "This will install all dependencies needed to run the game."
echo ""

echo ""
echo "Installing Python dependencies..."
echo ""

echo "[1/3] Installing client dependencies..."
python3 -m pip install -r requirements.txt

echo ""
echo "[2/3] Installing server dependencies..."
python3 -m pip install -r server/requirements.txt

echo ""
echo "[3/3] Installing build tools (optional, for creating executables)..."
python3 -m pip install pyinstaller

echo ""
echo "============================================================"
echo "Setup Complete!"
echo "============================================================"
echo ""
echo "You can now run:"
echo "  - python3 launcher.py    (Recommended: Easy launcher GUI)"
echo "  - python3 start_server.py   (Just start the server)"
echo "  - python3 multiplayer_main.py   (Just play multiplayer)"
echo "  - python3 modern_main.py   (Just play single player)"
echo ""
echo "Or build executables by running the build_exe.py script"
echo ""
