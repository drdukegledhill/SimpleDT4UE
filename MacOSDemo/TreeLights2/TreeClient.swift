//
//  TreeClient.swift
//  TreeLights2
//
//  Created by Duke Gledhill on 06/05/2025.
//


import Foundation
import Network
import Combine

class TreeClient: ObservableObject {
    private var connection: NWConnection?
    let host: String
    let port: UInt16
    
    @Published var isConnected = false
    @Published var errorMessage: String?
    @Published var connectionState: String = "Initializing"

    init(host: String = "192.168.178.195", port: UInt16 = 65436) {
        self.host = host
        self.port = port
    }

    func connect() {
        connectionState = "Creating connection..."
        print("[TreeClient] Attempting to connect to \(host):\(port)")
        let parameters = NWParameters.tcp
        let endpoint = NWEndpoint.hostPort(host: NWEndpoint.Host(host), port: NWEndpoint.Port(integerLiteral: port))
        connection = NWConnection(to: endpoint, using: parameters)

        connection?.stateUpdateHandler = { [weak self] state in
            DispatchQueue.main.async {
                print("[TreeClient] Connection state: \(state)")
                switch state {
                case .preparing:
                    self?.connectionState = "Preparing connection..."
                case .ready:
                    self?.isConnected = true
                    self?.errorMessage = nil
                    self?.connectionState = "Connected"
                    print("[TreeClient] Connected to \(self?.host ?? ""):\(self?.port ?? 0)")
                case .failed(let error):
                    self?.isConnected = false
                    self?.errorMessage = "Connection failed: \(error.localizedDescription)"
                    self?.connectionState = "Failed"
                    print("[TreeClient] Connection failed: \(error)")
                case .waiting(let error):
                    self?.errorMessage = "Waiting: \(error.localizedDescription)"
                    self?.connectionState = "Waiting"
                    print("[TreeClient] Connection waiting: \(error)")
                case .cancelled:
                    self?.isConnected = false
                    self?.errorMessage = "Connection cancelled"
                    self?.connectionState = "Cancelled"
                    print("[TreeClient] Connection cancelled")
                default:
                    self?.connectionState = "State: \(state)"
                    print("[TreeClient] Connection state: \(state)")
                }
            }
        }

        connection?.start(queue: .main)
    }

    func disconnect() {
        connection?.cancel()
        connection = nil
        isConnected = false
        errorMessage = nil
    }

    func setPixel(_ index: Int, color: [Double]) {
        guard isConnected else {
            errorMessage = "Not connected to server"
            return
        }
        let command: [String: Any] = [
            "type": "set_pixel",
            "pixel": index,
            "color": color
        ]
        sendCommand(command)
    }

    func setAllPixels(color: [Double]) {
        guard isConnected else {
            errorMessage = "Not connected to server"
            return
        }
        let command: [String: Any] = [
            "type": "set_all",
            "color": color
        ]
        sendCommand(command)
    }

    func off() {
        guard isConnected else {
            errorMessage = "Not connected to server"
            return
        }
        let command: [String: Any] = [
            "type": "off"
        ]
        sendCommand(command)
    }

    private func sendCommand(_ command: [String: Any]) {
        guard let data = try? JSONSerialization.data(withJSONObject: command) else {
            errorMessage = "Failed to serialize command"
            return
        }
        connection?.send(content: data, completion: .contentProcessed { [weak self] error in
            if let error = error {
                DispatchQueue.main.async {
                    self?.errorMessage = "Send error: \(error.localizedDescription)"
                    print("Send error: \(error)")
                }
            }
        })
    }
}