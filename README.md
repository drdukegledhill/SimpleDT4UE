# SimpleDT4VR - Simple Digital Twin for Virtual Reality

A low-cost, open-source digital twinning solution using a Christmas tree as a demonstration application. This project showcases real-time synchronization between multiple clients (Python, macOS, iOS, and Unity) communicating with a central Python server.

## Project Structure

The project is organized into several components:

- **UnityDemo/**: Unity-based 3D visualization of the digital twin
- **MacOSDemo/**: macOS application for controlling the digital twin
- **iOSDemo/**: iOS application for mobile control of the digital twin
- **PiServer/**: Python server implementation for Raspberry Pi
- **PythonDemo/**: Python client implementation

## Features

- Real-time synchronization between multiple clients
- Cross-platform compatibility (Windows, macOS, iOS, Linux)
- 3D visualization in Unity
- Mobile control interface
- Low-cost implementation using Raspberry Pi
- Open-source and easily adaptable for other digital twin applications

## Getting Started

### Prerequisites

- Unity 2022.3 LTS or later
- Python 3.8 or later
- Xcode 14 or later (for iOS/macOS development)
- Raspberry Pi (for server implementation)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/drdukegledhill/SimpleDT4VR.git
   ```

2. Set up the Python server:
   ```bash
   cd PiServer
   pip install -r requirements.txt
   python server.py
   ```

3. Open the Unity project:
   - Open Unity Hub
   - Add the UnityDemo directory
   - Open the project

4. Build and run the iOS/macOS applications:
   - Open the iOSDemo or MacOSDemo in Xcode
   - Build and run on your device

## Network Protocol

The system uses a simple TCP-based protocol for communication:

- Server listens on port 5000
- Clients connect and send/receive JSON messages
- Real-time updates for all connected clients

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Developed as part of the University of Huddersfield's digital twinning research
- Special thanks to the open-source community for their invaluable tools and libraries
