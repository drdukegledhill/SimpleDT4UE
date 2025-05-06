#!/usr/bin/env python3
"""
Generic network server for controlling physical devices.
Supports multiple device types through a common interface.
"""

import socket
import logging
import os
import json
import threading
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from tree import RGBXmasTree

# Constants for default configuration
DEFAULT_HOST = "0.0.0.0"  # Listen on all interfaces
DEFAULT_PORT = 65436
DEFAULT_DEVICE_TYPE = "rgb_tree"
DEFAULT_BUFFER_SIZE = 1024
DISCOVERY_PORT = 65435

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DeviceController(ABC):
    """Abstract base class for device controllers."""
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the device."""
        pass
    
    @abstractmethod
    def process_command(self, command: Dict[str, Any]) -> None:
        """Process a command for the device."""
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        """Clean up device resources."""
        pass

class RGBTreeController(DeviceController):
    """Controller for the RGB Christmas Tree."""
    
    def __init__(self):
        self.tree = None
    
    def initialize(self) -> None:
        """Initialize the RGB tree."""
        self.tree = RGBXmasTree()
        logger.info("RGB Tree initialized")
    
    def process_command(self, command: Dict[str, Any]) -> None:
        """Process a command for the RGB tree."""
        try:
            if command["type"] == "set_pixel":
                pixel = command["pixel"]
                color = command["color"]
                self.tree[pixel].color = color
            elif command["type"] == "set_all":
                color = command["color"]
                self.tree.color = color
            elif command["type"] == "off":
                self.tree.off()
            else:
                raise ValueError(f"Unknown command type: {command['type']}")
        except (KeyError, ValueError, IndexError) as e:
            logger.error(f"Error processing command: {e}")
            raise
    
    def cleanup(self) -> None:
        """Clean up the RGB tree."""
        if self.tree:
            self.tree.color = (0, 0, 0)
            self.tree.close()
            logger.info("RGB Tree cleaned up")

class DiscoveryServer:
    """Server that responds to discovery requests."""
    
    DISCOVERY_MSG = b"RGB_TREE_DISCOVERY"
    RESPONSE_MSG = b"RGB_TREE_HERE"

    def __init__(self):
        self.running = False
        self.socket = None
        self.thread = None

    def start(self):
        """Start the discovery server in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        logger.info("Discovery server started")

    def _run(self):
        """Run the discovery server."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', DISCOVERY_PORT))
        
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                if data == self.DISCOVERY_MSG:
                    logger.info(f"Received discovery request from {addr[0]}")
                    self.socket.sendto(self.RESPONSE_MSG, addr)
            except Exception as e:
                if self.running:
                    logger.error(f"Error in discovery server: {e}")

    def stop(self):
        """Stop the discovery server."""
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None
        if self.thread:
            self.thread.join(timeout=1.0)
        logger.info("Discovery server stopped")

class NetworkServer:
    """Generic network server for device control."""
    
    def __init__(self, host: str, port: int, device_type: str):
        self.host = host
        self.port = port
        self.device_type = device_type
        self.controller = self._create_controller()
        self.running = False
        self.discovery_server = DiscoveryServer()

    def _create_controller(self) -> DeviceController:
        """Create the appropriate device controller."""
        if self.device_type == "rgb_tree":
            return RGBTreeController()
        else:
            raise ValueError(f"Unknown device type: {self.device_type}")
    
    def handle_client(self, conn: socket.socket, addr: tuple) -> None:
        """Handle communication with a single client."""
        with conn:
            logger.info(f"Connected by {addr}")
            while self.running:
                try:
                    data = conn.recv(DEFAULT_BUFFER_SIZE).decode("utf-8")
                    if not data:
                        break
                    
                    # Parse the command
                    command = json.loads(data)
                    self.controller.process_command(command)
                    
                    # Send acknowledgment
                    conn.sendall(b"OK\n")
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from {addr}")
                    conn.sendall(b"ERROR: Invalid JSON format\n")
                except Exception as e:
                    logger.error(f"Error handling client {addr}: {e}")
                    conn.sendall(f"ERROR: {str(e)}\n".encode())
                    break
    
    def start(self) -> None:
        """Start the server."""
        self.running = True
        self.controller.initialize()
        self.discovery_server.start()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((self.host, self.port))
                s.listen()
                logger.info(f"Server started on {self.host}:{self.port}")
                
                while self.running:
                    try:
                        conn, addr = s.accept()
                        self.handle_client(conn, addr)
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        logger.error(f"Error accepting connection: {e}")
            finally:
                self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up server resources."""
        self.running = False
        self.discovery_server.stop()
        self.controller.cleanup()
        logger.info("Server stopped")

def main():
    """Main entry point."""
    # Get configuration from environment variables or use defaults
    host = os.getenv("HOST", DEFAULT_HOST)
    port = int(os.getenv("PORT", DEFAULT_PORT))
    device_type = os.getenv("DEVICE_TYPE", DEFAULT_DEVICE_TYPE)
    
    try:
        server = NetworkServer(host, port, device_type)
        server.start()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    main()
