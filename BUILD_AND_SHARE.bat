@echo off
cls
echo ============================================================
echo  Ready Set Bet - ONE-CLICK BUILD
echo ============================================================
echo.
echo This script will:
echo  1. Install all dependencies
echo  2. Build .exe files
echo  3. Tell you which files to share with friends
echo.
echo It takes about 10-15 minutes. Go grab a coffee!
echo.
pause

echo.
echo ============================================================
echo [Step 1/4] Upgrading pip...
echo ============================================================
python -m pip install --upgrade pip --quiet

echo.
echo ============================================================
echo [Step 2/4] Installing dependencies...
echo ============================================================
echo This may take a few minutes...
python -m pip install customtkinter Pillow websockets requests --quiet
python -m pip install fastapi uvicorn sqlalchemy python-dotenv pydantic --quiet
python -m pip install pyinstaller --quiet

echo.
echo ============================================================
echo [Step 3/4] Building .exe files...
echo ============================================================
echo This takes 10-15 minutes. Please wait...
echo.

REM Build the game client (what friends will use)
echo Building Game Client for friends...
pyinstaller --name="ReadySetBet-Game" ^
  --onefile ^
  --windowed ^
  --add-data="assets;assets" ^
  --add-data="src;src" ^
  --hidden-import=customtkinter ^
  --hidden-import=websockets ^
  --hidden-import=PIL ^
  --clean ^
  --noconfirm ^
  multiplayer_main.py

REM Build the launcher for you (host)
echo.
echo Building Launcher for you (the host)...
pyinstaller --name="ReadySetBet-Launcher" ^
  --onefile ^
  --windowed ^
  --add-data="assets;assets" ^
  --add-data="src;src" ^
  --add-data="server;server" ^
  --hidden-import=uvicorn ^
  --hidden-import=fastapi ^
  --hidden-import=websockets ^
  --hidden-import=sqlalchemy ^
  --hidden-import=customtkinter ^
  --hidden-import=PIL ^
  --clean ^
  --noconfirm ^
  launcher.py

echo.
echo ============================================================
echo [Step 4/4] Cleaning up...
echo ============================================================
REM Create a dist_final folder with just what's needed
if not exist "dist_final" mkdir dist_final
copy "dist\ReadySetBet-Game.exe" "dist_final\" >nul
copy "dist\ReadySetBet-Launcher.exe" "dist_final\" >nul

echo.
echo ============================================================
echo  SUCCESS! Everything is ready!
echo ============================================================
echo.
echo Your files are in the "dist_final" folder:
echo.
echo   FOR YOU (the host):
echo     dist_final\ReadySetBet-Launcher.exe
echo     ^- Double-click this to host games
echo.
echo   FOR YOUR FRIENDS:
echo     dist_final\ReadySetBet-Game.exe
echo     ^- Send this file to your friends (they just double-click it!)
echo.
echo ============================================================
echo  How to use:
echo ============================================================
echo.
echo 1. YOU: Double-click ReadySetBet-Launcher.exe
echo    - Click "Start Server"
echo    - Share the IP address it shows (e.g., ws://73.45.123.89:8000)
echo    - Click "Play Multiplayer" to join your own server
echo    - Create a session and share the code
echo.
echo 2. FRIENDS:
echo    - Double-click ReadySetBet-Game.exe
echo    - Enter your IP address
echo    - Enter the session code
echo    - Play!
echo.
echo ============================================================
echo.
echo NOTE: For friends to connect from the internet, you need to:
echo   1. Forward port 8000 in your router, OR
echo   2. Use Tailscale VPN (easier!) - see LAUNCHER_GUIDE.md
echo.
echo See LAUNCHER_GUIDE.md for detailed instructions.
echo.
echo Press any key to open the dist_final folder...
pause >nul
explorer dist_final
