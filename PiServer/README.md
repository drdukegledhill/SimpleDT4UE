# SimpleDT4UE - Raspberry Pi Server

This is the server component of the SimpleDT4UE project, designed to run on a Raspberry Pi. It manages the digital twin system and communicates with all client applications.

## Features
- TCP server for client communication
- Real-time state management
- Support for multiple concurrent clients
- Hardware control for physical tree lights

## Requirements
- Raspberry Pi (3B+ or newer recommended)
- Python 3.8 or newer
- Required Python packages (see requirements.txt)

## Setup
1. Clone this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```

## Network Configuration
- Default port: 5000
- Configure in server.py

## Project Structure
- `server.py` - Main server implementation
- `tree.py` - Tree state management
- `sequence.py` - Light sequence patterns
- `requirements.txt` - Python dependencies

## Contributing
Please refer to the main SimpleDT4UE repository for contribution guidelines. 