#!/usr/bin/env python3
"""
GUI Demo client for the RGB Christmas Tree server.
Provides a graphical interface to control individual pixels.
"""

import sys
import json
import time
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QSlider, QPushButton, 
                            QComboBox, QGridLayout, QSpacerItem, QSizePolicy,
                            QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette, QFont
from tree_client import TreeClient

class ColorPicker(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Color Controls")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Add some spacing
        layout.addSpacing(10)
        
        # Color sliders with labels
        for color, label in [("Red", "red_slider"), ("Green", "green_slider"), ("Blue", "blue_slider")]:
            color_layout = QVBoxLayout()
            color_label = QLabel(color)
            color_label.setFont(QFont("Arial", 12))
            color_layout.addWidget(color_label)
            
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 255)
            slider.setValue(0)
            slider.valueChanged.connect(self.update_color)
            slider.setStyleSheet("""
                QSlider::groove:horizontal {
                    border: 1px solid #999999;
                    height: 8px;
                    background: #f0f0f0;
                    margin: 2px 0;
                    border-radius: 4px;
                }
                QSlider::handle:horizontal {
                    background: #007AFF;
                    border: none;
                    width: 16px;
                    height: 16px;
                    margin: -4px 0;
                    border-radius: 8px;
                }
            """)
            color_layout.addWidget(slider)
            setattr(self, label, slider)
            layout.addLayout(color_layout)
        
        # Brightness slider
        brightness_layout = QVBoxLayout()
        brightness_label = QLabel("Brightness")
        brightness_label.setFont(QFont("Arial", 12))
        brightness_layout.addWidget(brightness_label)
        
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.update_color)
        self.brightness_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #f0f0f0;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #007AFF;
                border: none;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
        """)
        brightness_layout.addWidget(self.brightness_slider)
        layout.addLayout(brightness_layout)
        
        # Add some spacing
        layout.addSpacing(20)
        
        # Color preview
        preview_frame = QFrame()
        preview_frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Sunken)
        preview_layout = QVBoxLayout(preview_frame)
        
        preview_label = QLabel("Preview")
        preview_label.setFont(QFont("Arial", 12))
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(preview_label)
        
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(120, 120)
        self.color_preview.setStyleSheet("""
            background-color: black;
            border: 1px solid #999999;
            border-radius: 8px;
        """)
        preview_layout.addWidget(self.color_preview)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(preview_frame)
        
        self.setLayout(layout)
    
    def update_color(self):
        r = self.red_slider.value()
        g = self.green_slider.value()
        b = self.blue_slider.value()
        brightness = self.brightness_slider.value() / 100.0
        
        # Apply brightness
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        # Update preview
        self.color_preview.setStyleSheet(f"""
            background-color: rgb({r}, {g}, {b});
            border: 1px solid #999999;
            border-radius: 8px;
        """)
        
        # Get normalized color values (0-1)
        color = [r/255, g/255, b/255]
        
        # Update the selected pixel in real-time
        if self.parent:
            pixel = self.parent.get_selected_pixel()
            if pixel is not None:
                try:
                    self.parent.tree_client.set_pixel(pixel, color)
                    self.parent.pixel_colors[pixel] = color
                    self.parent.update_button_color(pixel, color)
                except Exception as e:
                    self.parent.statusBar().showMessage(f'Error: {str(e)}')
        
        return color

    def set_color(self, color: list):
        """Set the color picker to a specific color."""
        r, g, b = [int(c * 255) for c in color]
        self.red_slider.setValue(r)
        self.green_slider.setValue(g)
        self.blue_slider.setValue(b)
        self.brightness_slider.setValue(100)

class TreeControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tree_client = TreeClient()
        self.pixel_colors = [[0, 0, 0] for _ in range(25)]
        self.demo_running = False  # Add flag to control demo
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('RGB Tree Controller')
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f7;
            }
            QLabel {
                color: #1d1d1f;
            }
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-family: Arial;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #0071EB;
            }
            QPushButton:pressed {
                background-color: #0062CC;
            }
            QPushButton:disabled {
                background-color: #999999;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create horizontal layout for tree and color picker
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        # Left side: Tree layout
        left_panel = QWidget()
        left_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        tree_layout = QVBoxLayout(left_panel)
        tree_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("RGB Christmas Tree")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tree_layout.addWidget(title)
        
        # Add some spacing
        tree_layout.addSpacing(20)
        
        # Create pixel buttons
        self.pixel_buttons = [None] * 25
        
        # Star at the top (pixel 3)
        star_layout = QHBoxLayout()
        star_layout.addStretch()
        star_btn = self.create_pixel_button(3, "★")
        self.pixel_buttons[3] = star_btn
        star_layout.addWidget(star_btn)
        star_layout.addStretch()
        tree_layout.addLayout(star_layout)
        
        # Tree body (8 columns of 3 pixels)
        tree_body = QHBoxLayout()
        tree_body.setSpacing(10)
        
        # Create columns
        pixel_index = 0
        for col in range(8):
            col_layout = QVBoxLayout()
            col_layout.setSpacing(10)
            col_buttons = []
            
            for row in range(3):
                if pixel_index == 3:
                    pixel_index += 1
                current_index = pixel_index
                btn = self.create_pixel_button(current_index)
                self.pixel_buttons[current_index] = btn
                col_buttons.append(btn)
                pixel_index += 1
            
            if col % 2 == 0:
                for btn in reversed(col_buttons):
                    col_layout.addWidget(btn)
            else:
                for btn in col_buttons:
                    col_layout.addWidget(btn)
            
            tree_body.addLayout(col_layout)
        
        tree_layout.addLayout(tree_body)
        tree_layout.addStretch()
        
        # Right side: Color picker
        right_panel = QWidget()
        right_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 10px;
            }
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add color picker
        self.color_picker = ColorPicker(self)
        right_layout.addWidget(self.color_picker)
        right_layout.addStretch()
        
        # Add panels to content layout
        content_layout.addWidget(left_panel, 2)
        content_layout.addWidget(right_panel, 1)
        
        # Add content layout to main layout
        main_layout.addLayout(content_layout)
        
        # Create bottom panel for buttons
        bottom_panel = QWidget()
        bottom_panel.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
                border-radius: 10px;
            }
        """)
        bottom_layout = QHBoxLayout(bottom_panel)
        bottom_layout.setContentsMargins(20, 20, 20, 20)
        bottom_layout.setSpacing(10)
        
        # Add debug label
        debug_label = QLabel("Control Panel")
        debug_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        bottom_layout.addWidget(debug_label)
        
        # Add control buttons with more obvious styling
        self.off_selected_button = QPushButton('Turn Off Selected')
        self.off_selected_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #0071EB;
            }
            QPushButton:pressed {
                background-color: #0062CC;
            }
        """)
        self.off_selected_button.clicked.connect(self.turn_off_selected)
        bottom_layout.addWidget(self.off_selected_button)
        
        self.off_all_button = QPushButton('Turn Off All')
        self.off_all_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #0071EB;
            }
            QPushButton:pressed {
                background-color: #0062CC;
            }
        """)
        self.off_all_button.clicked.connect(self.turn_off_all)
        bottom_layout.addWidget(self.off_all_button)
        
        self.demo_button = QPushButton('Run Demo Sequence')
        self.demo_button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #0071EB;
            }
            QPushButton:pressed {
                background-color: #0062CC;
            }
        """)
        self.demo_button.clicked.connect(self.run_demo_sequence)
        bottom_layout.addWidget(self.demo_button)
        
        self.stop_demo_button = QPushButton('Stop Demo')
        self.stop_demo_button.setStyleSheet("""
            QPushButton {
                background-color: #999999;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #FF453A;
            }
            QPushButton:pressed {
                background-color: #FF2D55;
            }
        """)
        self.stop_demo_button.clicked.connect(self.stop_demo)
        self.stop_demo_button.setEnabled(False)  # Initially disabled
        bottom_layout.addWidget(self.stop_demo_button)
        
        bottom_layout.addStretch()
        
        # Add bottom panel to main layout
        main_layout.addWidget(bottom_panel)
        
        # Connect to the tree
        try:
            self.tree_client.connect()
            self.statusBar().showMessage('Connected to tree')
        except Exception as e:
            self.statusBar().showMessage(f'Connection error: {str(e)}')
    
    def create_pixel_button(self, index: int, text: str = None) -> QPushButton:
        """Create a pixel button with consistent styling."""
        btn = QPushButton(text or f'P{index}')
        btn.setCheckable(True)
        btn.clicked.connect(lambda checked, idx=index: self.select_pixel(idx))
        btn.setFixedSize(60, 60)
        btn.setStyleSheet("""
            QPushButton {
                border: 2px solid #e0e0e0;
                border-radius: 30px;
                background-color: black;
                color: white;
                font-family: Arial;
                font-size: 12px;
            }
            QPushButton:checked {
                border: 2px solid #007AFF;
            }
            QPushButton:hover {
                border-color: #007AFF;
            }
        """)
        return btn

    def update_button_color(self, index: int, color: list):
        """Update the color of a pixel button."""
        r, g, b = [int(c * 255) for c in color]
        self.pixel_buttons[index].setStyleSheet(f"""
            QPushButton {{
                border: 2px solid #e0e0e0;
                border-radius: 30px;
                background-color: rgb({r}, {g}, {b});
                color: {'white' if (r + g + b) < 384 else 'black'};
                font-family: Arial;
                font-size: 12px;
            }}
            QPushButton:checked {{
                border: 2px solid #007AFF;
            }}
            QPushButton:hover {{
                border-color: #007AFF;
            }}
        """)
    
    def select_pixel(self, index):
        """Select a pixel and update the color picker."""
        for btn in self.pixel_buttons:
            if btn is not None:
                btn.setChecked(btn == self.pixel_buttons[index])
        self.color_picker.set_color(self.pixel_colors[index])
    
    def get_selected_pixel(self):
        for i, btn in enumerate(self.pixel_buttons):
            if btn.isChecked():
                return i
        return None
    
    def turn_off_selected(self):
        pixel = self.get_selected_pixel()
        if pixel is not None:
            try:
                self.tree_client.set_pixel(pixel, [0, 0, 0])
                self.pixel_colors[pixel] = [0, 0, 0]
                self.update_button_color(pixel, [0, 0, 0])
                self.statusBar().showMessage(f'Turned off pixel {pixel}')
            except Exception as e:
                self.statusBar().showMessage(f'Error: {str(e)}')
    
    def turn_off_all(self):
        try:
            self.tree_client.off()
            for i in range(25):
                self.pixel_colors[i] = [0, 0, 0]
                self.update_button_color(i, [0, 0, 0])
            self.statusBar().showMessage('Turned off all pixels')
        except Exception as e:
            self.statusBar().showMessage(f'Error: {str(e)}')
    
    def stop_demo(self):
        """Stop the running demo sequence."""
        self.demo_running = False
        self.demo_button.setEnabled(True)
        self.stop_demo_button.setEnabled(False)
        self.stop_demo_button.setStyleSheet("""
            QPushButton {
                background-color: #999999;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #FF453A;
            }
            QPushButton:pressed {
                background-color: #FF2D55;
            }
        """)
        self.statusBar().showMessage('Demo stopped')
        self.turn_off_all()  # Turn off all lights when stopping
    
    def run_demo_sequence(self):
        """Run the demo sequence of animations."""
        try:
            self.demo_running = True
            self.demo_button.setEnabled(False)
            self.stop_demo_button.setEnabled(True)
            self.stop_demo_button.setStyleSheet("""
                QPushButton {
                    background-color: #FF3B30;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-size: 14px;
                    min-width: 150px;
                }
                QPushButton:hover {
                    background-color: #FF453A;
                }
                QPushButton:pressed {
                    background-color: #FF2D55;
                }
            """)
            self.statusBar().showMessage('Running demo sequence...')
            
            # Color wipes
            for color, name in [([1, 0, 0], 'red'), ([0, 1, 0], 'green'), ([0, 0, 1], 'blue')]:
                if not self.demo_running:
                    return
                self.statusBar().showMessage(f'Running {name} color wipe...')
                for i in range(25):
                    if not self.demo_running:
                        return
                    self.tree_client.set_pixel(i, color)
                    self.pixel_colors[i] = color
                    self.update_button_color(i, color)
                    QApplication.processEvents()
                    time.sleep(0.1)
                time.sleep(0.5)
            
            # Static rainbow pattern
            if self.demo_running:
                self.statusBar().showMessage('Setting rainbow pattern...')
                for i in range(25):
                    if not self.demo_running:
                        return
                    hue = i / 25.0  # Evenly distribute colors
                    r, g, b = self.hsv_to_rgb(hue, 1.0, 1.0)
                    self.tree_client.set_pixel(i, [r, g, b])
                    self.pixel_colors[i] = [r, g, b]
                    self.update_button_color(i, self.pixel_colors[i])
                    QApplication.processEvents()
                time.sleep(2)  # Show the pattern for 2 seconds
            
            # Sparkle effect
            if self.demo_running:
                self.statusBar().showMessage('Running sparkle effect...')
                for _ in range(50):  # 50 sparkles
                    if not self.demo_running:
                        return
                    pixel = random.randint(0, 24)
                    color = [random.random(), random.random(), random.random()]
                    self.tree_client.set_pixel(pixel, color)
                    self.pixel_colors[pixel] = color
                    self.update_button_color(pixel, color)
                    QApplication.processEvents()
                    time.sleep(0.1)
            
            if self.demo_running:
                self.statusBar().showMessage('Demo sequence completed')
                self.turn_off_all()  # Turn off all lights at the end
        except Exception as e:
            self.statusBar().showMessage(f'Error during demo: {str(e)}')
        finally:
            self.demo_running = False
            self.demo_button.setEnabled(True)
            self.stop_demo_button.setEnabled(False)
            self.stop_demo_button.setStyleSheet("""
                QPushButton {
                    background-color: #999999;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-size: 14px;
                    min-width: 150px;
                }
                QPushButton:hover {
                    background-color: #FF453A;
                }
                QPushButton:pressed {
                    background-color: #FF2D55;
                }
            """)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB color."""
        if s == 0.0:
            return v, v, v
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q

    def closeEvent(self, event):
        """Handle window close event."""
        try:
            self.turn_off_all()
            self.tree_client.disconnect()
            self.statusBar().showMessage('Lights turned off and disconnected')
        except Exception as e:
            self.statusBar().showMessage(f'Error during shutdown: {str(e)}')
        finally:
            event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application-wide font
    app.setFont(QFont("Arial", 13))
    
    window = TreeControlWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 