@echo off
cls
echo ============================================================
echo  Ready Set Bet - ONE-CLICK BUILD
echo ============================================================
echo.
echo This script will:
echo  1. Install all dependencies
echo  2. Build ONE .exe file that does EVERYTHING
echo  3. Tell you which file to share with friends
echo.
echo It takes about 10-15 minutes. Go grab a coffee!
echo.
pause

echo.
echo ============================================================
echo [Step 1/3] Upgrading pip...
echo ============================================================
python -m pip install --upgrade pip --quiet

echo.
echo ============================================================
echo [Step 2/3] Installing dependencies...
echo ============================================================
echo This may take a few minutes...
python -m pip install customtkinter Pillow websockets requests --quiet
python -m pip install fastapi uvicorn sqlalchemy python-dotenv pydantic --quiet
python -m pip install pyinstaller --quiet

echo.
echo ============================================================
echo [Step 3/3] Building ONE .exe file...
echo ============================================================
echo This takes 10-15 minutes. Please wait...
echo.

REM Build the unified launcher (ONLY .exe needed!)
echo Building Ready Set Bet (all-in-one)...
pyinstaller --name="ReadySetBet" ^
  --onefile ^
  --windowed ^
  --add-data="assets;assets" ^
  --add-data="src;src" ^
  --add-data="server;server" ^
  --hidden-import=customtkinter ^
  --hidden-import=websockets ^
  --hidden-import=PIL ^
  --hidden-import=uvicorn ^
  --hidden-import=uvicorn.logging ^
  --hidden-import=uvicorn.loops ^
  --hidden-import=uvicorn.loops.auto ^
  --hidden-import=uvicorn.protocols ^
  --hidden-import=uvicorn.protocols.http ^
  --hidden-import=uvicorn.protocols.http.auto ^
  --hidden-import=uvicorn.lifespan ^
  --hidden-import=uvicorn.lifespan.on ^
  --hidden-import=fastapi ^
  --hidden-import=sqlalchemy ^
  --hidden-import=sqlalchemy.ext.declarative ^
  --hidden-import=pydantic ^
  --hidden-import=starlette ^
  --collect-all=uvicorn ^
  --collect-all=fastapi ^
  --clean ^
  --noconfirm ^
  unified_launcher.py

echo.
echo ============================================================
echo Cleaning up...
echo ============================================================
REM Create a dist_final folder with just the ONE .exe
if not exist "dist_final" mkdir dist_final
copy "dist\ReadySetBet.exe" "dist_final\" >nul

echo.
echo ============================================================
echo  SUCCESS! Everything is ready!
echo ============================================================
echo.
echo Your file is in the "dist_final" folder:
echo.
echo   dist_final\ReadySetBet.exe
echo   ^- This is the ONLY file you need!
echo   ^- You AND your friends use this same file
echo.
echo ============================================================
echo  How to use:
echo ============================================================
echo.
echo FOR YOU (the host):
echo   1. Double-click ReadySetBet.exe
echo   2. Click "Host a Game"
echo   3. Server starts automatically
echo   4. You'll see your IP and session code
echo   5. Share both with friends!
echo.
echo FOR FRIENDS:
echo   1. Double-click ReadySetBet.exe
echo   2. Click "Join a Friend's Game"
echo   3. Enter your IP and session code
echo   4. Play!
echo.
echo ============================================================
echo.
echo NOTE: For friends to connect from the internet, you need to:
echo   1. Forward port 8000 in your router, OR
echo   2. Use Tailscale VPN (easier!) - see LAUNCHER_GUIDE.md
echo.
echo Send "ReadySetBet.exe" to your friends and you're done!
echo.
echo Press any key to open the dist_final folder...
pause >nul
explorer dist_final
