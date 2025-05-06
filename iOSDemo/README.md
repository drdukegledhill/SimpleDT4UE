# iOS Digital Twin Demo

A native iOS application for controlling the SimpleDT4UE digital twin system. This demo provides a mobile interface for interacting with the digital twin using a Christmas tree as the demonstration object.

## Features

- Native iOS interface
- Real-time state synchronization
- Interactive light control
- Network status monitoring
- Support for both iPhone and iPad

## Requirements

- iOS 15.0 or later
- Xcode 14.0 or later
- Swift 5.7 or later

## Setup

1. Open the project in Xcode
2. Select your target device/simulator
3. Configure the server hostname in the app settings
4. Build and run the application

## Controls

- Tap on lights to toggle their state
- Use the settings panel to configure the server connection
- Monitor connection status in the status bar
- Support for both portrait and landscape orientations

## Network Protocol

The application communicates with the server using a simple TCP-based protocol:
- Connects to `simpledigitaltwin.local:65436`
- Sends/receives JSON messages for state updates
- Maintains real-time synchronization

## Development

### Project Structure

- `TreeLightsMobile/`
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
- Verify the server hostname is correct
- Ensure your device is on the same network as the server

## License

This project is licensed under the MIT License - see the LICENSE file for details. 