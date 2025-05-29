#!/usr/bin/env python3
"""
IP Address Checker for MongoDB Atlas Whitelist
"""

import requests
import socket

def get_public_ip():
    """Get your public IP address."""
    try:
        # Try multiple services
        services = [
            'https://api.ipify.org',
            'https://ipinfo.io/ip',
            'https://icanhazip.com',
            'https://ident.me'
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                if response.status_code == 200:
                    ip = response.text.strip()
                    print(f"✓ Your public IP address: {ip}")
                    return ip
            except:
                continue
        
        print("✗ Could not determine public IP address")
        return None
        
    except Exception as e:
        print(f"✗ Error getting public IP: {e}")
        return None

def get_local_ip():
    """Get your local IP address."""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"✓ Your local IP address: {local_ip}")
        return local_ip
    except Exception as e:
        print(f"✗ Error getting local IP: {e}")
        return None

def main():
    print("IP Address Information for MongoDB Atlas Whitelist")
    print("=" * 50)
    
    public_ip = get_public_ip()
    local_ip = get_local_ip()
    
    print("\n" + "=" * 50)
    print("INSTRUCTIONS:")
    print("=" * 50)
    print("1. Go to https://cloud.mongodb.com")
    print("2. Select your 'fitrack-db' cluster")
    print("3. Click 'Network Access' in the left sidebar")
    print("4. Click 'Add IP Address'")
    print("5. Add your public IP address:")
    if public_ip:
        print(f"   → {public_ip}")
    print("6. Or temporarily add 0.0.0.0/0 (allows all IPs - less secure)")
    print("7. Click 'Confirm'")
    print("8. Wait for the changes to take effect (1-2 minutes)")
    print("9. Try running your Django server again")

if __name__ == "__main__":
    main()
