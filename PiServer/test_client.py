#!/usr/bin/env python3
"""
Simple test client for the device control server.
"""

import socket
import json
import time
import sys

def send_command(host: str, port: int, command: dict) -> None:
    """Send a command to the server and print the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            s.sendall(json.dumps(command).encode())
            response = s.recv(1024).decode()
            print(f"Response: {response.strip()}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    """Main entry point."""
    host = "localhost"
    port = 65436

    # Test commands
    commands = [
        {"type": "set_pixel", "pixel": 0, "color": [1.0, 0.0, 0.0]},  # Red
        {"type": "set_pixel", "pixel": 1, "color": [0.0, 1.0, 0.0]},  # Green
        {"type": "set_pixel", "pixel": 2, "color": [0.0, 0.0, 1.0]},  # Blue
        {"type": "set_all", "color": [1.0, 1.0, 0.0]},  # Yellow
        {"type": "off"}
    ]

    print("Testing server...")
    for cmd in commands:
        print(f"\nSending command: {cmd}")
        send_command(host, port, cmd)
        time.sleep(1)  # Wait a second between commands

if __name__ == "__main__":
    main() 