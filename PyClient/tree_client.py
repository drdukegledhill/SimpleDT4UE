#!/usr/bin/env python3
"""
TreeClient class for communicating with the RGB Christmas Tree server.
"""

import socket
import json
from typing import List

class TreeClient:
    def __init__(self, host: str = "simpledigitaltwin.local", port: int = 65436):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self) -> None:
        """Connect to the tree server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
        except socket.gaierror as e:
            raise ConnectionError(f"Could not resolve hostname {self.host}. Make sure the Raspberry Pi is running and the hostname is correct.") from e
        except ConnectionRefusedError as e:
            raise ConnectionError(f"Connection refused to {self.host}:{self.port}. Make sure the server is running.") from e

    def disconnect(self) -> None:
        """Disconnect from the tree server."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected from server")

    def send_command(self, command: dict) -> None:
        """Send a command to the tree server."""
        if not self.socket:
            raise ConnectionError("Not connected to server")
        
        self.socket.sendall(json.dumps(command).encode())
        response = self.socket.recv(1024).decode()
        print(f"Response: {response.strip()}")

    def set_pixel(self, pixel: int, color: List[float]) -> None:
        """Set a single pixel to a specific color."""
        self.send_command({
            "type": "set_pixel",
            "pixel": pixel,
            "color": color
        })

    def set_all(self, color: List[float]) -> None:
        """Set all pixels to a specific color."""
        self.send_command({
            "type": "set_all",
            "color": color
        })

    def off(self) -> None:
        """Turn all pixels off."""
        self.send_command({"type": "off"}) 