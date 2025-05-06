# macOS Digital Twin Demo

A native macOS application for controlling the SimpleDT4UE digital twin system. This demo provides a desktop interface for interacting with the digital twin using a Christmas tree as the demonstration object.

## Features

- Native macOS interface
- Real-time state synchronization
- Interactive light control
- Network status monitoring

## Requirements

- macOS 12.0 or later
- Xcode 14.0 or later
- Swift 5.7 or later

## Setup

1. Open the project in Xcode
2. Select your target device/simulator
3. Configure the server IP address in the app settings
4. Build and run the application

## Controls

- Click on lights to toggle their state
- Use the server configuration panel to set the connection details
- Monitor connection status in the status bar

## Network Protocol

The application communicates with the server using a simple TCP-based protocol:
- Connects to the server on port 5000
- Sends/receives JSON messages for state updates
- Maintains real-time synchronization

## Development

### Project Structure

- `TreeLights2/`
  - `ContentView.swift`: Main user interface
  - `TreeClient.swift`: Network communication
  - `Models/`: Data models and state management

### Building

1. Open the project in Xcode
2. Select your target device
3. Click the Run button or press Cmd+R

## Troubleshooting

- Ensure the server is running before starting the client
- Check the console for network connection errors
- Verify the server IP address is correct

## License

This project is licensed under the MIT License - see the LICENSE file for details. 