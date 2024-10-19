import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt6.QtCore import Qt
import serial


class STM32ControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.serial_port = None

    def initUI(self):
        # Set window properties
        self.setWindowTitle('STM32 Controller')
        self.setGeometry(100, 100, 400, 200)

        # Create main widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for the window
        layout = QVBoxLayout()

        # Create a label to display status
        self.status_label = QLabel('Status: Disconnected')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Create input for serial port
        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText('Enter COM Port (e.g., COM3 or /dev/ttyUSB0)')
        layout.addWidget(self.port_input)

        # Create a button to connect to the STM32
        self.connect_button = QPushButton('Connect to STM32', self)
        self.connect_button.clicked.connect(self.connect_to_stm32)
        layout.addWidget(self.connect_button)

        # Create a button to send a command
        self.send_button = QPushButton('Send Command', self)
        self.send_button.clicked.connect(self.send_command)
        self.send_button.setEnabled(False)
        layout.addWidget(self.send_button)

        # Set the layout for the widget
        central_widget.setLayout(layout)

    def connect_to_stm32(self):
        """Connect to the STM32 board using the specified COM port."""
        port = self.port_input.text()
        try:
            # Open serial port
            self.serial_port = serial.Serial(port, baudrate=115200, timeout=1)
            self.status_label.setText(f'Status: Connected to {port}')
            self.send_button.setEnabled(True)
        except serial.SerialException:
            self.status_label.setText('Status: Failed to connect')

    def send_command(self):
        """Send a predefined command to the STM32 board."""
        if self.serial_port and self.serial_port.is_open:
            try:
                command = 'LED_ON\n'  # Example command
                self.serial_port.write(command.encode())
                self.status_label.setText('Status: Command sent')
            except Exception as e:
                self.status_label.setText(f'Status: Failed to send command: {e}')

    def closeEvent(self, event):
        """Ensure serial port is closed when the app is closed."""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = STM32ControlApp()
    ex.show()
    sys.exit(app.exec())
