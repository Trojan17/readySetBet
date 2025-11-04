@echo off
echo ============================================================
echo Ready Set Bet - Building .exe Files
echo ============================================================
echo.
echo This will create standalone .exe files you can run anywhere!
echo No Python installation needed to run the .exe files.
echo.
pause

echo.
echo Installing dependencies...
python -m pip install -r requirements.txt
python -m pip install -r server/requirements.txt
python -m pip install pyinstaller

echo.
echo Building executables...
python build_exe.py

echo.
echo ============================================================
echo Done! Check the 'dist' folder for your .exe files.
echo ============================================================
pause
