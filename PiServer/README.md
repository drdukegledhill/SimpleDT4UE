# Raspberry Pi Digital Twin Server

The central server component of the SimpleDT4UE project, designed to run on a Raspberry Pi. This server manages the state of the digital twin and coordinates communication between all clients.

## Features

- Centralized state management
- Real-time client synchronization
- TCP-based communication
- Low resource usage
- Designed for Raspberry Pi

## Requirements

- Raspberry Pi (3 or 4 recommended)
- Python 3.8 or later
- Raspbian OS or Raspberry Pi OS

## Setup

1. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the server:
   - Edit `server.py` to set your preferences
   - Default port is 5000

3. Start the server:
   ```bash
   python server.py
   ```

## Network Protocol

The server implements a simple TCP-based protocol:
- Listens on port 5000
- Accepts multiple client connections
- Broadcasts state updates to all connected clients
- Uses JSON for message formatting

## Development

### Project Structure

- `server.py`: Main server implementation and configuration
- `requirements.txt`: Python dependencies

### Building

No build step required - the server runs directly with Python.

## Troubleshooting

- Check the server logs for connection issues
- Ensure the port is not blocked by a firewall
- Verify client IP addresses are correct
- Monitor system resources (CPU, memory)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 