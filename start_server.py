"""
Simple Server Launcher - Just run this to start the server!
No Docker or complex setup needed.
"""
import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the Ready Set Bet server"""
    print("=" * 60)
    print("🎰 Ready Set Bet - Multiplayer Server")
    print("=" * 60)
    print()
    print("Starting server...")
    print("Server will be available at: http://0.0.0.0:8000")
    print()
    print("Share this with friends to connect:")

    # Get public IP
    try:
        import requests
        public_ip = requests.get('https://api.ipify.org', timeout=3).text
        print(f"  ws://{public_ip}:8000")
    except:
        print("  ws://YOUR_IP_ADDRESS:8000")
        print("  (Find your IP at: https://whatismyipaddress.com)")

    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Start uvicorn
    import uvicorn
    uvicorn.run(
        "server.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
