#!/usr/bin/env python3
"""
Demo client for the RGB Christmas Tree server.
Shows various patterns and animations that can be sent to the tree.
"""

import socket
import json
import time
import random
import math
from typing import List, Tuple

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

    def rainbow_wave(self, duration: float = 10.0) -> None:
        """Create a rainbow wave effect."""
        start_time = time.time()
        while time.time() - start_time < duration:
            for i in range(25):  # 25 pixels in the tree
                hue = (i / 25.0 + (time.time() - start_time) / 5.0) % 1.0
                r, g, b = self.hsv_to_rgb(hue, 1.0, 1.0)
                self.set_pixel(i, [r, g, b])
            time.sleep(0.05)

    def sparkle(self, duration: float = 10.0) -> None:
        """Create a sparkle effect."""
        start_time = time.time()
        while time.time() - start_time < duration:
            # Randomly select pixels to light up
            for _ in range(5):  # Light up 5 pixels at a time
                pixel = random.randint(0, 24)
                color = [random.random(), random.random(), random.random()]
                self.set_pixel(pixel, color)
            time.sleep(0.1)
            self.off()
            time.sleep(0.1)

    def color_wipe(self, color: List[float], duration: float = 2.0) -> None:
        """Wipe a color across all pixels."""
        delay = duration / 25.0  # 25 pixels
        for i in range(25):
            self.set_pixel(i, color)
            time.sleep(delay)

    def breathing(self, color: List[float], duration: float = 5.0) -> None:
        """Create a breathing effect with a specific color."""
        start_time = time.time()
        while time.time() - start_time < duration:
            # Calculate brightness using a sine wave
            brightness = (math.sin((time.time() - start_time) * 2) + 1) / 2
            dimmed_color = [c * brightness for c in color]
            self.set_all(dimmed_color)
            time.sleep(0.05)

    @staticmethod
    def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[float, float, float]:
        """Convert HSV to RGB color."""
        if s == 0.0:
            return v, v, v
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6

        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

def main():
    """Run the demo."""
    # Create client with DNS name
    client = TreeClient(host="simpledigitaltwin.local")  # Using mDNS name
    
    try:
        client.connect()
        
        print("\nDemo 1: Color Wipe")
        client.color_wipe([1.0, 0.0, 0.0])  # Red
        time.sleep(1)
        client.color_wipe([0.0, 1.0, 0.0])  # Green
        time.sleep(1)
        client.color_wipe([0.0, 0.0, 1.0])  # Blue
        time.sleep(1)
        
        print("\nDemo 2: Breathing Effect")
        client.breathing([1.0, 0.0, 0.0])  # Red breathing
        time.sleep(1)
        
        print("\nDemo 3: Rainbow Wave")
        client.rainbow_wave()
        time.sleep(1)
        
        print("\nDemo 4: Sparkle Effect")
        client.sparkle()
        time.sleep(1)
        
        print("\nDemo Complete!")
        client.off()
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main() 