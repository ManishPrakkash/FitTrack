#!/usr/bin/env python
"""
Simple utility to display your local IP address.
This helps when connecting from a mobile device to your local development server.
"""

import socket
import sys

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Create a socket connection to an external server
        # This is a reliable way to get the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable, just needs to be a valid address
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None

if __name__ == "__main__":
    ip = get_local_ip()
    if ip:
        print("\n=== LOCAL IP ADDRESS INFORMATION ===\n")
        print(f"Your local IP address is: {ip}")
        print("\nTo connect from your phone to your local development server:")
        print(f"1. Make sure your phone is on the same WiFi network as this computer")
        print(f"2. Update the API configuration in your frontend code:")
        print(f"   return 'http://{ip}:8000';")
        print("\n3. Run your Django server with:")
        print(f"   python manage.py runserver 0.0.0.0:8000")
        print("\nThis will make your server accessible from other devices on your network.")
    else:
        print("Could not determine local IP address.")
        sys.exit(1)
