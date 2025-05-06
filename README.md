# SimpleDT4UE - Simple Digital Twin for Unity Engine

A low-cost, open-source digital twinning solution using a Christmas tree as a demonstration application. This project showcases real-time digital twinning with multiple client applications communicating with a central server.

## Project Structure

The project is split into multiple repositories:

1. [Unity Demo](UnityDemo/) - 3D visualization client
2. [macOS Demo](MacOSDemo/) - Native macOS client
3. [iOS Demo](iOSDemo/) - Native iOS client
4. [Raspberry Pi Server](PiServer/) - Central server implementation
5. [Python Demo](PythonDemo/) - Python reference client

## Features

- Real-time digital twinning
- Multiple client platforms:
  - Unity (3D visualization)
  - macOS (native app)
  - iOS (mobile app)
  - Python (reference implementation)
- Centralized server on Raspberry Pi
- TCP-based communication
- Cross-platform compatibility

## Getting Started

1. Clone the desired repositories
2. Follow the setup instructions in each repository's README
3. Start the Raspberry Pi server
4. Run any of the client applications

## Network Protocol

All clients communicate with the server using a simple TCP-based protocol:
- Default port: 5000
- JSON-based message format
- Real-time state synchronization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Unity Technologies for the game engine
- Raspberry Pi Foundation for the server platform
- Apple for the iOS/macOS development tools
