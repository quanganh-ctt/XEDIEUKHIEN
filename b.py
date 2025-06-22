import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QTextEdit
)
from PyQt5.QtCore import Qt, QTimer


class RobotGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚗 Điều khiển Robot Bluetooth - Quang Anh (TRẠNG THÁI XE)")
        self.resize(520, 500)

        self.fake_serial_mode = True  # ✅ 
        self.serial = None
        self.init_ui()

    def init_ui(self):
        # --- Tiêu đề ---
        self.title_label = QLabel("👤 Người dùng: Quang Anh")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: blue")

        # --- (Ẩn) Chọn COM ---
        self.port_label = QLabel("🔌 Chế độ: ĐÃ KẾT NỐI ")
        self.connect_btn = QPushButton("Kết nối HEHEHE")
        self.connect_btn.setEnabled(False)

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
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

        # --- Nút Di chuyển ngẫu nhiên ---
        self.random_btn = QPushButton("🎲 Di chuyển ngẫu nhiên")
        self.random_btn.setCheckable(True)
        self.random_btn.clicked.connect(self.toggle_random_move)

        # --- Layout tổng ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(port_layout)
        main_layout.addWidget(self.distance_label)
        main_layout.addLayout(top)
        main_layout.addLayout(mid)
        main_layout.addLayout(bot)
        main_layout.addWidget(self.random_btn)
        main_layout.addWidget(QLabel("🖥️ Phản hồi (TRẠNG THÁI XE):"))
        main_layout.addWidget(self.log_box)

        self.setLayout(main_layout)

        # --- Timer cập nhật dữ liệu THẠT---
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
        self.timer.start(1000)  # cập nhật mỗi giây

        # --- Timer gửi lệnh random ---
        self.random_timer = QTimer()
        self.random_timer.timeout.connect(self.send_random_command)

    def send_command(self, command):
        self.log_box.append(f"▶ (TRẠNG THÁI XE) Gửi lệnh: {command}")

    def read_serial_data(self):
        fake_distance = round(random.uniform(15.0, 80.0), 1)
        self.log_box.append(f"← (TRẠNG THÁI XE) Khoảng cách: {fake_distance} cm")
        self.distance_label.setText(f"📏 Khoảng cách: {fake_distance} cm")

    def toggle_random_move(self):
        if self.random_btn.isChecked():
            self.random_btn.setText("⏹️ Dừng ngẫu nhiên")
            self.random_timer.start(1000)  # mỗi 1 giây
            self.log_box.append("🎲 Bắt đầu di chuyển ngẫu nhiên.")
        else:
            self.random_timer.stop()
            self.random_btn.setText("🎲 Di chuyển ngẫu nhiên")
            self.log_box.append("⏹️ Dừng di chuyển ngẫu nhiên.")

    def send_random_command(self):
        command_list = list(self.buttons.keys())
        command_list.remove('S')  # Không random lệnh dừng
        cmd = random.choice(command_list)
        self.send_command(cmd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RobotGUI()
    window.show()
    sys.exit(app.exec_())
