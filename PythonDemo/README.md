# Python Digital Twin Demo

A Python-based client implementation for the SimpleDT4UE project. This demo provides a reference implementation of the client protocol and can be used as a starting point for custom Python clients.

## Features

- Simple TCP client implementation
- Real-time state synchronization
- Command-line interface
- Cross-platform compatibility
- Easy to extend and modify

## Requirements

- Python 3.8 or later
- Required packages (see requirements.txt)

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure the client:
   - Edit the server IP address in the script
   - Default port is 5000

3. Run the client:
   ```bash
   python tree_client.py
   ```

## Network Protocol

The client implements a simple TCP-based protocol:
- Connects to the server on port 5000
- Sends/receives JSON messages
- Maintains real-time synchronization

## Development

### Project Structure

- `tree_client.py`: Main client implementation
- `requirements.txt`: Python dependencies

### Building

No build step required - the client runs directly with Python.

## Troubleshooting

- Ensure the server is running
- Check network connectivity
- Verify the server IP address
- Check the console for error messages

## License

This project is licensed under the MIT License - see the LICENSE file for details. 