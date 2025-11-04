@echo off
echo ============================================================
echo Ready Set Bet - Simple Setup (Minimal Dependencies)
echo ============================================================
echo.
echo This installs only the essential packages needed to run.
echo If you had build errors before, this should fix them!
echo.
pause

echo.
echo Step 1: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 2: Installing core client dependencies...
python -m pip install customtkinter Pillow websockets requests

echo.
echo Step 3: Installing server dependencies...
python -m pip install fastapi uvicorn websockets sqlalchemy python-dotenv pydantic requests

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo You can now run:
echo   python launcher.py
echo.
echo If you still have errors, see TROUBLESHOOTING.md
echo.
pause
