# Unity Digital Twin Demo

A Unity-based 3D visualization client for the SimpleDT4UE project. This demo showcases real-time digital twinning using a Christmas tree as the demonstration object.

## Features

- Real-time 3D visualization
- Interactive light control
- Network synchronization
- Cross-platform compatibility

## Requirements

- Unity 2022.3 LTS or later
- .NET Standard 2.1
- TCP/IP networking support

## Setup

1. Open the project in Unity Hub
2. Open the main scene in `Assets/Scenes/Main.unity`
3. Configure the server IP address in the TreeClient component
4. Press Play to start the visualization

## Controls

- Left-click and drag to rotate the camera
- Right-click and drag to pan
- Scroll to zoom in/out
- Click on lights to toggle their state

## Network Protocol

The client communicates with the server using a simple TCP-based protocol:
- Connects to `simpledigitaltwin.local:65436`
- Sends/receives JSON messages for state updates
- Maintains real-time synchronization

## Development

### Project Structure

- `Assets/Scripts/`
  - `TreeClient.cs`: Network communication
  - `TreeLightController.cs`: Light state management
  - `TreeLightUI.cs`: User interface controls

### Building

1. Open the project in Unity
2. Go to File > Build Settings
3. Select your target platform
4. Click Build

## Troubleshooting

- Ensure the server is running before starting the client
- Check the console for network connection errors
- Verify the server hostname is correct

## License

This project is licensed under the MIT License - see the LICENSE file for details. 