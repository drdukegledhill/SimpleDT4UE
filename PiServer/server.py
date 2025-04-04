# echo-server.py

import socket
import threading
import logging
import os
from tree import RGBXmasTree
from time import sleep

# Constants for default configuration
DEFAULT_HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
DEFAULT_PORT = 65436  # Port to listen on (non-privileged ports are > 1023)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the tree
tree = RGBXmasTree()

# Get host and port from environment variables or use defaults
HOST = os.getenv("HOST", DEFAULT_HOST)
PORT = int(os.getenv("PORT", DEFAULT_PORT))

def updateTree(datastring):
    """Update the tree's LED colors based on the received data string."""
    try:
        brokenstring = datastring.split(",")
        if len(brokenstring) != 4:
            raise ValueError("Invalid data format")
        tree[int(brokenstring[0])].color = (
            float(brokenstring[1]),
            float(brokenstring[2]),
            float(brokenstring[3]),
        )
    except (ValueError, IndexError) as e:
        logger.error(f"Error updating tree: {e}")

def close(s):
    """Gracefully close the socket and reset the tree."""
    try:
        s.shutdown(socket.SHUT_RDWR)
    except Exception as e:
        logger.warning(f"Error shutting down socket: {e}")
    finally:
        s.close()
        tree.color = (0, 0, 0)
        logger.info("Server closed")

def handle_client(conn, addr):
    """Handle communication with a single client."""
    with conn:
        logger.info(f"Connected by {addr}")
        while True:
            try:
                data = conn.recv(1024).decode("utf-8")
                if not data:
                    break
                updateTree(data)
            except Exception as e:
                logger.error(f"Error handling client {addr}: {e}")
                break
    logger.info(f"Connection with {addr} closed")

def start_server():
    """Start the server and listen for incoming connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
            s.listen()
            logger.info(f"Server started on {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr)).start()
        except Exception as e:
            logger.error(f"Server error: {e}")
        finally:
            close(s)

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        tree.color = (0, 0, 0)
        logger.info("Tree reset and server stopped")
