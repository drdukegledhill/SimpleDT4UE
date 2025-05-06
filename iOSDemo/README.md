# SimpleDT4UE - iOS Demo

This is the iOS client component of the SimpleDT4UE project. It provides a native iOS application for controlling the digital twin system.

## Features
- Native iOS UI using SwiftUI
- TCP networking for server communication
- Real-time tree light control
- Support for iOS 15.0 and newer

## Requirements
- iOS 15.0 or newer
- Xcode 14.0 or newer
- Swift 5.7 or newer

## Setup
1. Clone this repository
2. Open TreeLightsMobile.xcodeproj in Xcode
3. Build and run the project on a simulator or device

## Network Configuration
- Default server address: localhost
- Default port: 5000
- Configure these in the TreeClient.swift file

## Project Structure
- `TreeClient.swift` - TCP networking implementation
- `ContentView.swift` - Main UI implementation

## Contributing
Please refer to the main SimpleDT4UE repository for contribution guidelines. 