#!/usr/bin/env python3
"""
GUI Demo client for the RGB Christmas Tree server.
Provides a graphical interface to control individual pixels.
"""

import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QSlider, QPushButton, 
                            QComboBox, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from tree_client import TreeClient

class ColorPicker(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Red slider
        self.red_slider = QSlider(Qt.Orientation.Horizontal)
        self.red_slider.setRange(0, 255)
        self.red_slider.setValue(0)
        self.red_slider.valueChanged.connect(self.update_color)
        
        # Green slider
        self.green_slider = QSlider(Qt.Orientation.Horizontal)
        self.green_slider.setRange(0, 255)
        self.green_slider.setValue(0)
        self.green_slider.valueChanged.connect(self.update_color)
        
        # Blue slider
        self.blue_slider = QSlider(Qt.Orientation.Horizontal)
        self.blue_slider.setRange(0, 255)
        self.blue_slider.setValue(0)
        self.blue_slider.valueChanged.connect(self.update_color)
        
        # Brightness slider
        self.brightness_slider = QSlider(Qt.Orientation.Horizontal)
        self.brightness_slider.setRange(0, 100)
        self.brightness_slider.setValue(100)
        self.brightness_slider.valueChanged.connect(self.update_color)
        
        # Color preview
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(100, 100)
        self.color_preview.setStyleSheet("background-color: black; border: 1px solid gray;")
        
        # Add widgets to layout
        layout.addWidget(QLabel("Red"))
        layout.addWidget(self.red_slider)
        layout.addWidget(QLabel("Green"))
        layout.addWidget(self.green_slider)
        layout.addWidget(QLabel("Blue"))
        layout.addWidget(self.blue_slider)
        layout.addWidget(QLabel("Brightness"))
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.color_preview)
        
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
        self.color_preview.setStyleSheet(
            f"background-color: rgb({r}, {g}, {b}); border: 1px solid gray;"
        )
        
        # Return normalized color values (0-1)
        return [r/255, g/255, b/255]

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
        self.pixel_colors = [[0, 0, 0] for _ in range(25)]  # Track colors for each pixel
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('RGB Tree Controller')
        self.setGeometry(100, 100, 1000, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Left side: Tree layout
        left_panel = QWidget()
        tree_layout = QVBoxLayout(left_panel)
        
        # Create pixel buttons
        self.pixel_buttons = []
        
        # Star at the top (pixel 3)
        star_layout = QHBoxLayout()
        star_layout.addStretch()
        star_btn = self.create_pixel_button(3, "★")
        star_layout.addWidget(star_btn)
        star_layout.addStretch()
        tree_layout.addLayout(star_layout)
        
        # Tree body (8 columns of 3 pixels)
        tree_body = QHBoxLayout()
        
        # Create columns
        for col in range(8):
            col_layout = QVBoxLayout()
            for row in range(3):
                pixel_num = col * 3 + row
                if pixel_num != 3:  # Skip the star pixel
                    btn = self.create_pixel_button(pixel_num)
                    col_layout.addWidget(btn)
            tree_body.addLayout(col_layout)
        
        tree_layout.addLayout(tree_body)
        
        # Right side: Color picker
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Add color picker
        self.color_picker = ColorPicker()
        right_layout.addWidget(self.color_picker)
        
        # Add control buttons
        control_layout = QHBoxLayout()
        
        self.apply_button = QPushButton('Apply Color')
        self.apply_button.clicked.connect(self.apply_color)
        control_layout.addWidget(self.apply_button)
        
        self.off_button = QPushButton('Turn Off')
        self.off_button.clicked.connect(self.turn_off)
        control_layout.addWidget(self.off_button)
        
        right_layout.addLayout(control_layout)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 2)  # Give more space to the tree
        main_layout.addWidget(right_panel, 1)
        
        # Connect to the tree
        try:
            self.tree_client.connect()
            self.statusBar().showMessage('Connected to tree')
        except Exception as e:
            self.statusBar().showMessage(f'Connection error: {str(e)}')
    
    def create_pixel_button(self, index: int, text: str = None) -> QPushButton:
        """Create a pixel button with consistent styling."""
        btn = QPushButton(text or f'Pixel {index}')
        btn.setCheckable(True)
        btn.clicked.connect(lambda checked, idx=index: self.select_pixel(idx))
        btn.setFixedSize(60, 60)
        btn.setStyleSheet("""
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: black;
                color: white;
                font-size: 12px;
            }
            QPushButton:checked {
                border: 2px solid #0078d7;
            }
        """)
        self.pixel_buttons.append(btn)
        return btn

    def update_button_color(self, index: int, color: list):
        """Update the color of a pixel button."""
        r, g, b = [int(c * 255) for c in color]
        self.pixel_buttons[index].setStyleSheet(f"""
            QPushButton {{
                border: 2px solid #8f8f91;
                border-radius: 6px;
                background-color: rgb({r}, {g}, {b});
                color: {'white' if (r + g + b) < 384 else 'black'};
            }}
            QPushButton:checked {{
                border: 2px solid #0078d7;
            }}
        """)
    
    def select_pixel(self, index):
        # Uncheck all other buttons
        for i, btn in enumerate(self.pixel_buttons):
            btn.setChecked(i == index)
        
        # Update color picker to show current color
        self.color_picker.set_color(self.pixel_colors[index])
    
    def get_selected_pixel(self):
        for i, btn in enumerate(self.pixel_buttons):
            if btn.isChecked():
                return i
        return None
    
    def apply_color(self):
        pixel = self.get_selected_pixel()
        if pixel is not None:
            color = self.color_picker.update_color()
            try:
                self.tree_client.set_pixel(pixel, color)
                self.pixel_colors[pixel] = color
                self.update_button_color(pixel, color)
                self.statusBar().showMessage(f'Set pixel {pixel} to color {color}')
            except Exception as e:
                self.statusBar().showMessage(f'Error: {str(e)}')
    
    def turn_off(self):
        try:
            self.tree_client.off()
            # Update all buttons to black
            for i in range(25):
                self.pixel_colors[i] = [0, 0, 0]
                self.update_button_color(i, [0, 0, 0])
            self.statusBar().showMessage('Turned off all pixels')
        except Exception as e:
            self.statusBar().showMessage(f'Error: {str(e)}')
    
    def closeEvent(self, event):
        """Handle window close event."""
        try:
            # Turn off all lights
            self.tree_client.off()
            # Update all buttons to black
            for i in range(25):
                self.pixel_colors[i] = [0, 0, 0]
                self.update_button_color(i, [0, 0, 0])
            # Disconnect from server
            self.tree_client.disconnect()
            self.statusBar().showMessage('Lights turned off and disconnected')
        except Exception as e:
            self.statusBar().showMessage(f'Error during shutdown: {str(e)}')
        finally:
            event.accept()

def main():
    app = QApplication(sys.argv)
    window = TreeControlWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 