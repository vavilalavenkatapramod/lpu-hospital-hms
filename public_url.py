"""
Script to create a public URL for your LPU Hospital Management System
using ngrok tunnel
"""
from pyngrok import ngrok

# Set your ngrok auth token here (get it from https://dashboard.ngrok.com/auth)
# If you don't have one, sign up for free at https://ngrok.com/
NGROK_AUTH_TOKEN = "YOUR_NGROK_AUTH_TOKEN_HERE"

def start_tunnel():
    """Start ngrok tunnel to expose local server"""
    
    # Configure ngrok
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    
    # Open tunnel to the local server
    public_url = ngrok.connect(8000, "http")
    
    print(f"\n🎉 Your LPU Hospital Management System is now live!")
    print(f"🌐 Public URL: {public_url}")
    print(f"\nShare this URL with anyone to access your app from anywhere in the world!")
    print(f"\nPress Ctrl+C to stop the tunnel\n")
    
    return public_url

if __name__ == "__main__":
    # Check if user has set their auth token
    if NGROK_AUTH_TOKEN == "YOUR_NGROK_AUTH_TOKEN_HERE":
        print("⚠️  Please add your ngrok auth token to this file first!")
        print("   1. Go to https://dashboard.ngrok.com/signup")
        print("   2. Sign up for a free account")
        print("   3. Copy your auth token from https://dashboard.ngrok.com/auth")
        print("   4. Replace 'YOUR_NGROK_AUTH_TOKEN_HERE' in this file with your token")
        print("   5. Run this script again")
    else:
        start_tunnel()
