//
//  ContentView.swift
//  TreeLights2
//
//  Created by Duke Gledhill on 06/05/2025.
//

import SwiftUI

struct Pixel: Identifiable {
    let id: Int
    var color: Color
    var brightness: Double
}

struct ContentView: View {
    @StateObject private var treeClient = TreeClient(host: "192.168.178.195", port: 65436)
    @State private var isDemoRunning = false
    @State private var stopDemoRequested = false
    @State private var selectedPixel: Int? = nil
    @State private var pixelColors: [Int: (Color, Double)] = (0..<25).reduce(into: [:]) { $0[$1] = (.black, 1.0) }

    var body: some View {
        VStack(spacing: 20) {
            Text("RGB Tree Controller")
                .font(.title)
                .padding(.top)

            // Tree Layout
            VStack(spacing: 10) {
                // Star (pixel 3)
                HStack {
                    Spacer()
                    pixelButton(for: 3, isStar: true)
                    Spacer()
                }
                // 8 columns of 3 pixels
                HStack(alignment: .top, spacing: 12) {
                    ForEach(0..<8) { col in
                        VStack(spacing: 12) {
                            ForEach((col % 2 == 0 ? [2,1,0] : [0,1,2]), id: \ .self) { row in
                                let idx = pixelIndex(col: col, row: row)
                                if idx < 25 && idx != 3 {
                                    pixelButton(for: idx)
                                } else {
                                    Spacer().frame(height: 44)
                                }
                            }
                        }
                    }
                }
            }
            .padding(.vertical)

            // Color and Brightness Controls
            if let selected = selectedPixel {
                VStack(spacing: 12) {
                    Text(selected == 3 ? "Star" : "Pixel \(selected)")
                        .font(.headline)
                    ColorPicker("Color", selection: Binding(
                        get: { pixelColors[selected]?.0 ?? .black },
                        set: { newColor in
                            let brightness = pixelColors[selected]?.1 ?? 1.0
                            pixelColors[selected] = (newColor, brightness)
                            sendPixelUpdate(selected)
                        }
                    ))
                    HStack {
                        Text("Brightness")
                        Slider(value: Binding(
                            get: { pixelColors[selected]?.1 ?? 1.0 },
                            set: { newBrightness in
                                let color = pixelColors[selected]?.0 ?? .black
                                pixelColors[selected] = (color, newBrightness)
                                sendPixelUpdate(selected)
                            }
                        ), in: 0...1)
                    }
                }
                .padding()
                .background(Color.gray.opacity(0.1))
                .cornerRadius(10)
            }

            // Control Buttons
            HStack(spacing: 16) {
                Button("Turn Off Selected") {
                    if let selected = selectedPixel {
                        pixelColors[selected] = (.black, 1.0)
                        sendPixelUpdate(selected)
                    }
                }
                .disabled(selectedPixel == nil)
                Button("Turn Off All") {
                    for i in 0..<25 {
                        pixelColors[i] = (.black, 1.0)
                    }
                    treeClient.off()
                }
                Button(isDemoRunning ? "Running Demo..." : "Demo") {
                    if !isDemoRunning {
                        runDemo()
                    }
                }
                .disabled(isDemoRunning || !treeClient.isConnected)
                if isDemoRunning {
                    Button("Stop Demo") {
                        stopDemoRequested = true
                    }
                    .tint(.red)
                }
            }
            .buttonStyle(.borderedProminent)
            .padding(.top)

            Spacer()
        }
        .padding()
        .onAppear {
            treeClient.connect()
        }
        .onDisappear {
            treeClient.off()
            treeClient.disconnect()
        }
    }

    // MARK: - Helpers
    func pixelButton(for idx: Int, isStar: Bool = false) -> some View {
        let (color, brightness) = pixelColors[idx] ?? (.black, 1.0)
        return Button(action: { selectedPixel = idx }) {
            ZStack {
                Circle()
                    .fill(color.opacity(brightness))
                    .frame(width: isStar ? 44 : 36, height: isStar ? 44 : 36)
                    .overlay(
                        Circle().stroke(selectedPixel == idx ? Color.blue : Color.gray, lineWidth: selectedPixel == idx ? 3 : 1)
                    )
                if isStar {
                    Text("★").font(.system(size: 24)).foregroundColor(.yellow)
                }
            }
        }
        .buttonStyle(.plain)
    }

    func pixelIndex(col: Int, row: Int) -> Int {
        // Map columns and rows to pixel indices, skipping 3 for the star
        var idx = col * 3 + row
        if idx >= 3 { idx += 1 }
        return idx
    }

    func sendPixelUpdate(_ idx: Int) {
        let (color, brightness) = pixelColors[idx] ?? (.black, 1.0)
        let rgb = colorToRGB(color: color, brightness: brightness)
        treeClient.setPixel(idx, color: rgb)
    }

    func colorToRGB(color: Color, brightness: Double) -> [Double] {
        let nsColor = NSColor(color)
        var r: CGFloat = 0, g: CGFloat = 0, b: CGFloat = 0, a: CGFloat = 0
        nsColor.getRed(&r, green: &g, blue: &b, alpha: &a)
        return [Double(r) * brightness, Double(g) * brightness, Double(b) * brightness]
    }

    func runDemo() {
        isDemoRunning = true
        stopDemoRequested = false
        DispatchQueue.global(qos: .userInitiated).async {
            // Color wipes: red, green, blue
            let colors: [[Double]] = [
                [1, 0, 0], [0, 1, 0], [0, 0, 1]
            ]
            for color in colors {
                for i in 0..<25 {
                    if stopDemoRequested { finishDemo(); return }
                    treeClient.setPixel(i, color: color)
                    usleep(100_000) // 0.1s
                }
                usleep(500_000) // 0.5s
            }
            // Static rainbow
            for i in 0..<25 {
                if stopDemoRequested { finishDemo(); return }
                let hue = Double(i) / 25.0
                let rgb = hsvToRgb(h: hue, s: 1.0, v: 1.0)
                treeClient.setPixel(i, color: rgb)
            }
            usleep(2_000_000) // 2s
            // Sparkle effect
            for _ in 0..<50 {
                if stopDemoRequested { finishDemo(); return }
                let pixel = Int.random(in: 0..<25)
                let color = [Double.random(in: 0...1), Double.random(in: 0...1), Double.random(in: 0...1)]
                treeClient.setPixel(pixel, color: color)
                usleep(100_000)
            }
            // Turn off all
            treeClient.off()
            finishDemo()
        }
    }

    func finishDemo() {
        DispatchQueue.main.async {
            isDemoRunning = false
            stopDemoRequested = false
            for i in 0..<25 {
                pixelColors[i] = (.black, 1.0)
            }
            treeClient.off()
        }
    }

    func hsvToRgb(h: Double, s: Double, v: Double) -> [Double] {
        if s == 0.0 { return [v, v, v] }
        let i = Int(h * 6.0)
        let f = (h * 6.0) - Double(i)
        let p = v * (1.0 - s)
        let q = v * (1.0 - s * f)
        let t = v * (1.0 - s * (1.0 - f))
        switch i % 6 {
        case 0: return [v, t, p]
        case 1: return [q, v, p]
        case 2: return [p, v, t]
        case 3: return [p, q, v]
        case 4: return [t, p, v]
        case 5: return [v, p, q]
        default: return [v, v, v]
        }
    }
}

#Preview {
    ContentView()
}
