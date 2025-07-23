import random
import sys
from typing import Dict

from PySide6.QtCore import Qt, Slot, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QVBoxLayout, 
                               QWidget, QHBoxLayout, QGraphicsDropShadowEffect)
from PySide6.QtGui import QColor


class ModernButton(QPushButton):
    """Custom button with modern styling and hover effects"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setupStyle()
    
    def setupStyle(self):
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00b4db, stop:1 #0083b0);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 200px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0083b0, stop:1 #00b4db);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #006d92, stop:1 #0077a3);
            }
        """)


class AnimatedLabel(QLabel):
    """Custom label with animation capabilities"""
    
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setupStyle()
        self.setupAnimation()
    
    def setupStyle(self):
        self.setStyleSheet("""
            QLabel {
                color: #2d3748;
                font-size: 28px;
                font-weight: bold;
                padding: 20px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                border: 2px solid rgba(0, 180, 219, 0.3);
                min-height: 80px;
            }
        """)
        self.setAlignment(Qt.AlignCenter)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)
    
    def setupAnimation(self):
        # Fade animation
        self.fadeAnimation = QPropertyAnimation(self, b"windowOpacity")
        self.fadeAnimation.setDuration(300)
        self.fadeAnimation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Scale animation would require more complex setup, so we'll use a timer for simple effects
        self.pulseTimer = QTimer()
        self.pulseTimer.timeout.connect(self.pulseEffect)
        
    def animateTextChange(self, new_text: str):
        """Animate text change with fade effect"""
        # First fade out
        self.fadeAnimation.setStartValue(1.0)
        self.fadeAnimation.setEndValue(0.3)
        self.fadeAnimation.finished.connect(lambda: self.changeTextAndFadeIn(new_text))
        self.fadeAnimation.start()
    
    def changeTextAndFadeIn(self, new_text: str):
        """Change text and fade back in"""
        self.setText(new_text)
        self.fadeAnimation.finished.disconnect()
        self.fadeAnimation.setStartValue(0.3)
        self.fadeAnimation.setEndValue(1.0)
        self.fadeAnimation.start()
        
        # Add pulse effect
        self.pulseTimer.start(100)
        QTimer.singleShot(500, self.pulseTimer.stop)
    
    def pulseEffect(self):
        """Simple pulse effect by changing stylesheet"""
        current_style = self.styleSheet()
        if "border: 3px solid" in current_style:
            # Return to normal
            self.setStyleSheet(current_style.replace("border: 3px solid", "border: 2px solid"))
        else:
            # Pulse
            self.setStyleSheet(current_style.replace("border: 2px solid", "border: 3px solid"))


class SmartHomeApp(QWidget):
    """Smart home control application with modern UI and animations"""
    
    def __init__(self):
        super().__init__()
        self.devices: Dict[str, str] = {
            "Living Room Light": "Off",
            "Thermostat": "22°C",
            "Security System": "Disarmed"
        }
        
        self.current_device = "Living Room Light"
        self.setupUI()
        self.setupWindow()
    
    def setupWindow(self):
        """Configure main window properties"""
        self.setWindowTitle("🏠 Smart Home Control")
        self.resize(500, 400)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #74ebd5, stop:0.5 #acb6e5, stop:1 #86a8e7);
            }
        """)
    
    def setupUI(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title = QLabel("🏠 Smart Home Control")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 10px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Device status display
        self.status_label = AnimatedLabel(f"{self.current_device}: {self.devices[self.current_device]}")
        
        # Device indicator
        self.device_label = QLabel(f"Current Device: {self.current_device}")
        self.device_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 8px 15px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        self.device_label.setAlignment(Qt.AlignCenter)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Toggle light button
        self.toggle_button = ModernButton("💡 Toggle Light")
        self.toggle_button.clicked.connect(self.toggleLight)
        
        # Set thermostat button
        self.thermostat_button = ModernButton("🌡️ Set Thermostat")
        self.thermostat_button.clicked.connect(self.setThermostat)
        self.thermostat_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff7e5f, stop:1 #feb47b);
                border: none;
                border-radius: 25px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 150px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #feb47b, stop:1 #ff7e5f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e66b4f, stop:1 #e59b6b);
            }
        """)
        
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.thermostat_button)
        
        # Statistics
        self.stats_label = QLabel("Actions performed: 0")
        self.stats_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                background: transparent;
                border: none;
                padding: 5px;
            }
        """)
        self.stats_label.setAlignment(Qt.AlignCenter)
        self.action_count = 0
        
        # Add widgets to main layout
        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.device_label)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.stats_label)
    
    @Slot()
    def toggleLight(self):
        """Toggle the light state and update UI"""
        # Cycle to next device
        device_list = list(self.devices.keys())
        current_index = device_list.index(self.current_device)
        self.current_device = device_list[(current_index + 1) % len(device_list)]
        
        # Toggle light if current device is a light
        if self.current_device == "Living Room Light":
            self.devices["Living Room Light"] = "On" if self.devices["Living Room Light"] == "Off" else "Off"
        
        self.action_count += 1
        
        # Update status label with animation
        self.status_label.animateTextChange(f"{self.current_device}: {self.devices[self.current_device]}")
        
        # Update device and stats labels
        QTimer.singleShot(150, lambda: self.updateInfoLabels(self.current_device))
    
    @Slot()
    def setThermostat(self):
        """Set thermostat temperature and update UI"""
        # Cycle to next device
        device_list = list(self.devices.keys())
        current_index = device_list.index(self.current_device)
        self.current_device = device_list[(current_index + 1) % len(device_list)]
        
        # Adjust thermostat if current device is thermostat
        if self.current_device == "Thermostat":
            current_temp = int(self.devices["Thermostat"].replace("°C", ""))
            new_temp = (current_temp + 1) % 30 if current_temp < 30 else 20  # Cycle between 20-30°C
            self.devices["Thermostat"] = f"{new_temp}°C"
        
        self.action_count += 1
        
        # Update status label with animation
        self.status_label.animateTextChange(f"{self.current_device}: {self.devices[self.current_device]}")
        
        # Update device and stats labels
        QTimer.singleShot(150, lambda: self.updateInfoLabels(self.current_device))
    
    def updateInfoLabels(self, device: str):
        """Update device and statistics labels"""
        self.device_label.setText(f"Current Device: {device}")
        self.stats_label.setText(f"Actions performed: {self.action_count}")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Smart Home Control")
    app.setOrganizationName("Smart Home Inc.")
    
    # Create and show widget
    widget = SmartHomeApp()
    widget.show()
    
    # Center window on screen
    screen_geometry = app.primaryScreen().availableGeometry()
    widget_geometry = widget.geometry()
    x = (screen_geometry.width() - widget_geometry.width()) // 2
    y = (screen_geometry.height() - widget_geometry.height()) // 2
    widget.move(x, y)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
