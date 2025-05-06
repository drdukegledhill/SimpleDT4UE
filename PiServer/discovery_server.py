#!/usr/bin/env python3
"""
Discovery server for the RGB Christmas Tree.
Responds to UDP broadcast requests to help clients find the tree on the network.
"""

import socket
import threading
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DiscoveryServer:
    DISCOVERY_PORT = 65435  # Must match the port in the client
    DISCOVERY_MSG = b"RGB_TREE_DISCOVERY"
    RESPONSE_MSG = b"RGB_TREE_HERE"

    def __init__(self):
        self.running = False
        self.socket = None

    def start(self):
        """Start the discovery server."""
        self.running = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind(('', self.DISCOVERY_PORT))
        
        logger.info(f"Discovery server started on port {self.DISCOVERY_PORT}")
        
        while self.running:
            try:
                data, addr = self.socket.recvfrom(1024)
                if data == self.DISCOVERY_MSG:
                    logger.info(f"Received discovery request from {addr[0]}")
                    self.socket.sendto(self.RESPONSE_MSG, addr)
            except Exception as e:
                if self.running:  # Only log if we're still supposed to be running
                    logger.error(f"Error in discovery server: {e}")

    def stop(self):
        """Stop the discovery server."""
        self.running = False
        if self.socket:
            self.socket.close()
            self.socket = None
        logger.info("Discovery server stopped")

def main():
    """Run the discovery server."""
    server = DiscoveryServer()
    try:
        server.start()
    except KeyboardInterrupt:
        logger.info("Discovery server interrupted by user")
    finally:
        server.stop()

if __name__ == "__main__":
    main() 