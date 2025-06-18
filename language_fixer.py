import sys
import os
import logging
from PyQt5.QtWidgets import (
    QApplication, QSystemTrayIcon, QMenu, QAction,
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
# logging.basicConfig(
#     filename="language_fixer.log",
#     level=logging.DEBUG,
#     format="%(asctime)s %(levelname)s: %(message)s"
# )
eng_to_thai = {
    '`': '_', '1': 'ๅ', '2': '/', '3': '-', '4': 'ภ', '5': 'ถ',
    '6': 'ุ', '7': 'ึ', '8': 'ค', '9': 'ต', '0': 'จ', '-': 'ข', '=': 'ช',
    'q': 'ๆ', 'w': 'ไ', 'e': 'ำ', 'r': 'พ', 't': 'ะ', 'y': 'ั', 'u': 'ี', 'i': 'ร', 'o': 'น', 'p': 'ย', '[': 'บ', ']': 'ล', '\\': 'ฃ',
    'a': 'ฟ', 's': 'ห', 'd': 'ก', 'f': 'ด', 'g': 'เ', 'h': '้', 'j': '่', 'k': 'า', 'l': 'ส', ';': 'ว', "'": 'ง',
    'z': 'ผ', 'x': 'ป', 'c': 'แ', 'v': 'อ', 'b': 'ิ', 'n': 'ื', 'm': 'ท', ',': 'ม', '.': 'ใ', '/': 'ฝ',
    # Shifted characters
    '~': '%', '!': '+', '@': '๑', '#': '๒', '$': '๓', '%': '๔', '^': 'ู', '&': '฿', '*': '๕', '(': '๖', ')': '๗', '_': '๘', '+': '๙',
    'Q': '๐', 'W': '"', 'E': 'ฎ', 'R': 'ฑ', 'T': 'ธ', 'Y': 'ํ', 'U': '๊', 'I': 'ณ', 'O': 'ฯ', 'P': 'ญ', '{': 'ฐ', '}': ',', '|': 'ฅ',
    'A': 'ฤ', 'S': 'ฆ', 'D': 'ฏ', 'F': 'โ', 'G': 'ฌ', 'H': '็', 'J': '๋', 'K': 'ษ', 'L': 'ศ', ':': 'ซ', '"': '.',
    'Z': '(', 'X': ')', 'C': 'ฉ', 'V': 'ฮ', 'B': 'ฺ', 'N': '์', 'M': '?', '<': 'ฒ', '>': 'ฬ', '?': 'ฦ'
}

class LanguageFixer:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        # Load tray icon
        icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
        if not os.path.exists(icon_path):
            print("ไม่พบไฟล์ icon.ico")
            sys.exit(1)
        icon = QIcon(icon_path)

        # Setup tray
        self.tray = QSystemTrayIcon(icon)
        self.tray.setToolTip("Language Fixer")
        self.tray.setVisible(True)

        # Context menu
        self.menu = QMenu()
        open_window_action = QAction("Open Translator")
        open_window_action.triggered.connect(self.show_window)
        quit_action = QAction("Quit")
        quit_action.triggered.connect(self.quit)

        self.menu.addAction(open_window_action)
        self.menu.addSeparator()
        self.menu.addAction(quit_action)
        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self.icon_clicked)
        self.window = self.create_window()
        self.tray.showMessage("Language Fixer", "Running in background", QSystemTrayIcon.Information, 3000)

    def icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:  # Left click
            self.show_window()

    def show_window(self):
        self.window.show()

    def quit(self):
        self.tray.hide()
        self.app.quit()

    def run(self):
        self.app.exec_()

    def create_window(self):
        window = QWidget()
        window.setWindowTitle("English to Thai Translator")
        window.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter English text...")
        layout.addWidget(self.input_box)

        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.output_label)

        convert_btn = QPushButton("Translate")
        convert_btn.clicked.connect(self.convert_word)
        layout.addWidget(convert_btn)

        window.setLayout(layout)
        return window

    def convert_text(self, text):
        result = ""
        for char in text:
            # แปลงทีละตัว ถ้าไม่มีใน dict ก็ใช้ตัวเดิม
            result += eng_to_thai.get(char, char)
        return result

    def convert_word(self):
        text = self.input_box.text()
        translation = self.convert_text(text)
        self.output_label.setText(f"➡ {translation}")

if __name__ == "__main__":
    try:
        app = LanguageFixer()
        app.run()
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"❌ Error: {str(e)}")
