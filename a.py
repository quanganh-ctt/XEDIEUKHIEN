import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer


class RobotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Điều khiển Robot Bluetooth - Quang Anh")
        self.resize(520, 450)

        self.serial = None
        self.init_ui()

    def init_ui(self):
        # --- Tiêu đề ---
        self.title_label = QLabel("👤 Người dùng: Quang Anh")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: blue")

        # --- Cổng COM ---
        self.port_label = QLabel("🔌 Chọn cổng COM:")
        self.port_combo = QComboBox()
        self.refresh_ports()

        self.connect_btn = QPushButton("Kết nối")
        self.connect_btn.clicked.connect(self.toggle_connection)

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.connect_btn)

        # --- Khoảng cách ---
        self.distance_label = QLabel("📏 Khoảng cách: -- cm")
        self.distance_label.setStyleSheet("font-size: 16px; color: green")

        # --- Điều khiển robot ---
        self.buttons = {
            'F': QPushButton("↑ Tiến"),
            'B': QPushButton("↓ Lùi"),
            'L': QPushButton("← Trái"),
            'R': QPushButton("→ Phải"),
            'I': QPushButton("↗ Tiến-Phải"),
            'G': QPushButton("↖ Tiến-Trái"),
            'J': QPushButton("↙ Lùi-Phải"),
            'H': QPushButton("↘ Lùi-Trái"),
            'S': QPushButton("■ Dừng")
        }

        for cmd, btn in self.buttons.items():
            btn.clicked.connect(lambda _, c=cmd: self.send_command(c))

        top = QHBoxLayout()
        mid = QHBoxLayout()
        bot = QHBoxLayout()

        top.addWidget(self.buttons['G'])
        top.addWidget(self.buttons['F'])
        top.addWidget(self.buttons['I'])

        mid.addWidget(self.buttons['L'])
        mid.addWidget(self.buttons['S'])
        mid.addWidget(self.buttons['R'])

        bot.addWidget(self.buttons['H'])
        bot.addWidget(self.buttons['B'])
        bot.addWidget(self.buttons['J'])

        # --- Log hiển thị dữ liệu ---
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)

        # --- Layout tổng ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(port_layout)
        main_layout.addWidget(self.distance_label)
        main_layout.addLayout(top)
        main_layout.addLayout(mid)
        main_layout.addLayout(bot)
        main_layout.addWidget(QLabel("🖥️ Phản hồi từ Arduino:"))
        main_layout.addWidget(self.log_box)

        self.setLayout(main_layout)

        # --- Timer đọc dữ liệu ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.port_combo.addItem(port.device)

    def toggle_connection(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.timer.stop()
            self.connect_btn.setText("Kết nối")
            self.log_box.append("❌ Đã ngắt kết nối.")
        else:
            try:
                port = self.port_combo.currentText()
                self.serial = serial.Serial(port, 9600, timeout=0.1)
                self.connect_btn.setText("Ngắt")
                self.timer.start(100)
                self.log_box.append(f"✅ Đã kết nối {port}")
            except Exception as e:
                self.log_box.append(f"Lỗi kết nối: {str(e)}")

    def send_command(self, command):
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(command.encode())
                self.log_box.append(f"▶ Gửi lệnh: {command}")
            except Exception as e:
                self.log_box.append(f"Lỗi gửi: {str(e)}")
        else:
            self.log_box.append("⚠️ Chưa kết nối Bluetooth!")

    def read_serial_data(self):
        if self.serial and self.serial.in_waiting:
            try:
                data = self.serial.readline().decode().strip()
                if data:
                    self.log_box.append(f"← {data}")
                    # Nếu dữ liệu là số → khoảng cách
                    if data.replace('.', '').isdigit():
                        self.distance_label.setText(f"📏 Khoảng cách: {data} cm")
                    elif data.startswith("D:"):
                        distance = data[2:].strip()
                        self.distance_label.setText(f"📏 Khoảng cách: {distance} cm")
            except Exception as e:
                self.log_box.append(f"Lỗi đọc dữ liệu: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotGUI()
    window.show()
    sys.exit(app.exec_())
