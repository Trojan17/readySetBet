@echo off
echo ============================================================
echo Ready Set Bet - Quick Setup
echo ============================================================
echo.
echo This will install all dependencies needed to run the game.
echo.
pause

echo.
echo Installing Python dependencies...
echo.

echo [1/3] Installing client dependencies...
python -m pip install -r requirements.txt

echo.
echo [2/3] Installing server dependencies...
python -m pip install -r server/requirements.txt

echo.
echo [3/3] Installing build tools (optional, for creating .exe)...
python -m pip install pyinstaller

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo You can now run:
echo   - python launcher.py    (Recommended: Easy launcher GUI)
echo   - python start_server.py   (Just start the server)
echo   - python multiplayer_main.py   (Just play multiplayer)
echo   - python modern_main.py   (Just play single player)
echo.
echo Or build .exe files by running: build_exe.bat
echo.
pause
