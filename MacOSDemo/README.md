# SimpleDT4UE - macOS Demo

This is the macOS client component of the SimpleDT4UE project. It provides a native macOS application for controlling the digital twin system.

## Features
- Native macOS UI using SwiftUI
- TCP networking for server communication
- Real-time tree light control
- System tray integration

## Requirements
- macOS 12.0 or newer
- Xcode 14.0 or newer
- Swift 5.7 or newer

## Setup
1. Clone this repository
2. Open TreeLights2.xcodeproj in Xcode
3. Build and run the project

## Network Configuration
- Default server address: localhost
- Default port: 5000
- Configure these in the TreeClient.swift file

## Project Structure
- `TreeClient.swift` - TCP networking implementation
- `ContentView.swift` - Main UI implementation

## Contributing
Please refer to the main SimpleDT4UE repository for contribution guidelines. 