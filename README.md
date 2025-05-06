# SimpleDT4UE (Simple Device Tree for Unreal Engine)

A flexible network server for controlling physical devices, with a focus on the RGB Christmas Tree and Unreal Engine integration.

## Overview

This project provides a simple TCP server that can control physical devices (currently supporting the RGB Christmas Tree) and can be integrated with Unreal Engine for interactive experiences. The server accepts JSON commands over TCP and translates them into device-specific actions.

## Features

- Generic device control interface
- JSON-based command protocol
- Support for RGB Christmas Tree
- Extensible architecture for adding new devices
- Unreal Engine integration support

## Requirements

### Server Requirements
- Python 3.6+
- Raspberry Pi (for RGB Tree control)
- Required Python packages:
  - gpiozero
  - colorzero

### Unreal Engine Requirements
- Unreal Engine 4.27 or later
- [TCP Socket Plugin](https://www.fab.com/listings/48db4522-8a05-4b91-bcf8-4217a698339b) from the Unreal Engine Marketplace

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/SimpleDT4UE.git
cd SimpleDT4UE
```

2. Install required Python packages:
```bash
pip install gpiozero colorzero
```

3. Purchase and install the TCP Socket Plugin from the Unreal Engine Marketplace:
   - Visit [TCP Socket Plugin](https://www.fab.com/listings/48db4522-8a05-4b91-bcf8-4217a698339b)
   - Add to your Unreal Engine project
   - Enable the plugin in your project settings

## Usage

### Starting the Server

```bash
# Start with default settings
python PiServer/server.py

# Or with custom settings
HOST=192.168.1.100 PORT=8080 DEVICE_TYPE=rgb_tree python PiServer/server.py
```

### Testing the Server

Use the provided test client:
```bash
python PiServer/test_client.py
```

Or send commands directly using netcat:
```bash
# Set a pixel to red
echo '{"type": "set_pixel", "pixel": 0, "color": [1.0, 0.0, 0.0]}' | nc localhost 65436

# Set all pixels to green
echo '{"type": "set_all", "color": [0.0, 1.0, 0.0]}' | nc localhost 65436

# Turn all pixels off
echo '{"type": "off"}' | nc localhost 65436
```

### Command Protocol

The server accepts JSON commands with the following format:

```json
// Set a single pixel
{
    "type": "set_pixel",
    "pixel": 0,
    "color": [1.0, 0.0, 0.0]  // [R, G, B] values from 0.0 to 1.0
}

// Set all pixels
{
    "type": "set_all",
    "color": [0.0, 1.0, 0.0]  // [R, G, B] values from 0.0 to 1.0
}

// Turn all pixels off
{
    "type": "off"
}
```

### Unreal Engine Integration

1. In your Unreal Engine project, add the TCP Socket Plugin to your project
2. Create a Blueprint that uses the TCP Socket component
3. Configure the socket to connect to your server's IP and port
4. Send JSON commands using the socket's Send String function

Example Blueprint setup:
1. Add TCP Socket component to your actor
2. Set the Remote Address to your server's IP
3. Set the Remote Port to your server's port (default: 65436)
4. Connect to the server
5. Use the Send String function to send JSON commands

## Adding New Devices

To add support for a new device:

1. Create a new class that inherits from `DeviceController`
2. Implement the required methods:
   - `initialize()`
   - `process_command(command)`
   - `cleanup()`
3. Add the new device type to the `_create_controller` method in `NetworkServer`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [The Pi Hut](https://thepihut.com/) for the RGB Christmas Tree
- [TCP Socket Plugin](https://www.fab.com/listings/48db4522-8a05-4b91-bcf8-4217a698339b) for Unreal Engine integration 