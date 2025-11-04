@echo off
cls
echo ============================================================
echo  CLEAN BUILD - Removing old files and rebuilding
echo ============================================================
echo.
echo This will:
echo  1. Delete old build artifacts
echo  2. Build a fresh .exe with the latest code
echo.
pause

echo.
echo ============================================================
echo [Step 1/4] Cleaning old build files...
echo ============================================================

REM Delete old build artifacts
if exist "build" (
    echo Deleting build folder...
    rmdir /s /q build
)

if exist "dist" (
    echo Deleting dist folder...
    rmdir /s /q dist
)

if exist "dist_final" (
    echo Deleting dist_final folder...
    rmdir /s /q dist_final
)

if exist "ReadySetBet.spec" (
    echo Deleting old spec file...
    del /q ReadySetBet.spec
)

echo ✓ Old files cleaned!

echo.
echo ============================================================
echo [Step 2/4] Upgrading pip...
echo ============================================================
python -m pip install --upgrade pip --quiet

echo.
echo ============================================================
echo [Step 3/4] Installing dependencies...
echo ============================================================
echo This may take a few minutes...
python -m pip install customtkinter Pillow websockets requests --quiet
python -m pip install fastapi uvicorn sqlalchemy python-dotenv pydantic --quiet
python -m pip install pyinstaller --quiet

echo.
echo ============================================================
echo [Step 4/4] Building FRESH .exe file...
echo ============================================================
echo This takes 10-15 minutes. Please wait...
echo.

REM Build with all the imports
echo Building ReadySetBet.exe with latest code...
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
echo Creating dist_final folder...
echo ============================================================
if not exist "dist_final" mkdir dist_final
copy "dist\ReadySetBet.exe" "dist_final\" >nul

echo.
echo ============================================================
echo  SUCCESS! Fresh build complete!
echo ============================================================
echo.
echo Your NEW file is here:
echo   dist_final\ReadySetBet.exe
echo.
echo This .exe has the latest code with programmatic uvicorn!
echo.
echo ============================================================
echo  Test it now:
echo ============================================================
echo   1. Close any old ReadySetBet.exe windows
echo   2. Run the NEW file: dist_final\ReadySetBet.exe
echo   3. Click "Host a Game"
echo   4. Check the logs - should say "Starting uvicorn server programmatically..."
echo.
echo Press any key to open the dist_final folder...
pause >nul
explorer dist_final
