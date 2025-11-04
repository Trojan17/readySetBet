"""
Build script to create .exe files for Ready Set Bet
Run this to package the game into standalone executables
"""
import PyInstaller.__main__
import os
import sys
import shutil

def build_launcher():
    """Build the main launcher.exe"""
    print("=" * 60)
    print("Building Launcher.exe...")
    print("=" * 60)

    PyInstaller.__main__.run([
        'launcher.py',
        '--name=ReadySetBet-Launcher',
        '--onefile',
        '--windowed',
        '--icon=assets/icon.png' if os.path.exists('assets/icon.png') else '--noconfirm',
        '--add-data=assets;assets',
        '--add-data=src;src',
        '--add-data=server;server',
        '--hidden-import=uvicorn',
        '--hidden-import=fastapi',
        '--hidden-import=websockets',
        '--hidden-import=sqlalchemy',
        '--clean',
    ])

def build_server():
    """Build the standalone server.exe"""
    print("=" * 60)
    print("Building Server.exe...")
    print("=" * 60)

    PyInstaller.__main__.run([
        'start_server.py',
        '--name=ReadySetBet-Server',
        '--onefile',
        '--console',
        '--icon=assets/icon.png' if os.path.exists('assets/icon.png') else '--noconfirm',
        '--add-data=server;server',
        '--add-data=src;src',
        '--hidden-import=uvicorn',
        '--hidden-import=fastapi',
        '--hidden-import=websockets',
        '--hidden-import=sqlalchemy',
        '--clean',
    ])

def build_client():
    """Build the game client.exe"""
    print("=" * 60)
    print("Building Game.exe...")
    print("=" * 60)

    PyInstaller.__main__.run([
        'multiplayer_main.py',
        '--name=ReadySetBet-Game',
        '--onefile',
        '--windowed',
        '--icon=assets/icon.png' if os.path.exists('assets/icon.png') else '--noconfirm',
        '--add-data=assets;assets',
        '--add-data=src;src',
        '--hidden-import=customtkinter',
        '--hidden-import=websockets',
        '--clean',
    ])

def build_single_player():
    """Build the single player game.exe"""
    print("=" * 60)
    print("Building SinglePlayer.exe...")
    print("=" * 60)

    PyInstaller.__main__.run([
        'modern_main.py',
        '--name=ReadySetBet-SinglePlayer',
        '--onefile',
        '--windowed',
        '--icon=assets/icon.png' if os.path.exists('assets/icon.png') else '--noconfirm',
        '--add-data=assets;assets',
        '--add-data=src;src',
        '--hidden-import=customtkinter',
        '--clean',
    ])

def main():
    """Main build process"""
    print("🎰 Ready Set Bet - Build .exe Files")
    print("=" * 60)
    print()
    print("This will create standalone .exe files you can share!")
    print()
    print("Files that will be created:")
    print("  1. ReadySetBet-Launcher.exe - All-in-one launcher")
    print("  2. ReadySetBet-Server.exe - Server only")
    print("  3. ReadySetBet-Game.exe - Multiplayer client only")
    print("  4. ReadySetBet-SinglePlayer.exe - Single player only")
    print()

    choice = input("Build all? (y/n): ").lower()

    if choice != 'y':
        print("Build cancelled.")
        return

    # Install PyInstaller if needed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")

    # Build all executables
    try:
        build_launcher()
        print("✅ Launcher.exe built successfully!\n")
    except Exception as e:
        print(f"❌ Error building Launcher: {e}\n")

    try:
        build_server()
        print("✅ Server.exe built successfully!\n")
    except Exception as e:
        print(f"❌ Error building Server: {e}\n")

    try:
        build_client()
        print("✅ Game.exe built successfully!\n")
    except Exception as e:
        print(f"❌ Error building Game: {e}\n")

    try:
        build_single_player()
        print("✅ SinglePlayer.exe built successfully!\n")
    except Exception as e:
        print(f"❌ Error building SinglePlayer: {e}\n")

    print("=" * 60)
    print("✅ Build complete!")
    print("=" * 60)
    print()
    print("Find your .exe files in the 'dist' folder:")
    print("  - ReadySetBet-Launcher.exe (Recommended - easiest to use)")
    print("  - ReadySetBet-Server.exe (Just the server)")
    print("  - ReadySetBet-Game.exe (Just the multiplayer client)")
    print("  - ReadySetBet-SinglePlayer.exe (Just single player)")
    print()
    print("You can now share these .exe files with friends!")
    print("No Python or dependencies needed to run them.")

if __name__ == "__main__":
    main()
