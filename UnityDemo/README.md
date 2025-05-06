# SimpleDT4UE - Unity Demo

This is the Unity client component of the SimpleDT4UE (Simple Digital Twin for Unity Engine) project. It provides a 3D visualization of the digital twin system using a Christmas tree as a demonstration.

## Features
- Real-time 3D visualization of the digital twin
- TCP networking for communication with the server
- Interactive UI controls for tree light manipulation
- Cross-platform compatibility

## Requirements
- Unity 2022.3 LTS or newer
- Universal Render Pipeline (URP)

## Setup
1. Clone this repository
2. Open the project in Unity
3. Open the SampleScene in Assets/Scenes
4. Press Play to run the demo

## Network Configuration
- Default server address: localhost
- Default port: 5000
- Configure these in the TreeClient component in the scene

## Project Structure
- `Assets/Scripts/TreeClient.cs` - TCP networking implementation
- `Assets/Scripts/TreeLightController.cs` - 3D tree visualization
- `Assets/Scripts/TreeLightUI.cs` - UI controls

## Contributing
Please refer to the main SimpleDT4UE repository for contribution guidelines. 