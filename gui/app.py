
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QComboBox, QRadioButton, QButtonGroup, QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

API_BASE = "http://127.0.0.1:8000"

class RedesignedApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Security Toolkit")
        self.setGeometry(100, 100, 800, 600)

        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel {
                font-size: 18px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
                background-color: #34495e;
                color: #ecf0f1;
            }
        """)

        self.stacked_widget = QStackedWidget()

        self.welcome_page = QWidget()
        self.sqli_page = QWidget()
        self.password_page = QWidget()
        self.encryption_page = QWidget()

        self.stacked_widget.addWidget(self.welcome_page)
        self.stacked_widget.addWidget(self.sqli_page)
        self.stacked_widget.addWidget(self.password_page)
        self.stacked_widget.addWidget(self.encryption_page)

        self.init_welcome_page()
        self.init_sqli_page()
        self.init_password_page()
        self.init_encryption_page()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)
    def init_password_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Password Strength Checker")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password to check...")
        self.password_result = QLabel("")

        check_button = QPushButton("Check")
        check_button.clicked.connect(self.check_password)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.welcome_page))

        layout.addWidget(title)
        layout.addSpacing(50)
        layout.addWidget(self.password_input)
        layout.addSpacing(20)
        layout.addWidget(check_button)
        layout.addSpacing(20)
        layout.addWidget(self.password_result)
        layout.addStretch()
        layout.addWidget(back_button)

        self.password_page.setLayout(layout)

    def check_password(self):
        password = self.password_input.text()
        try:
            r = requests.post(f"{API_BASE}/check_password", json={"password": password})
            data = r.json()
            self.password_result.setText(f"Strength: {data['strength']}")
        except requests.exceptions.RequestException as e:
            self.password_result.setText(f"Error: {e}")


    def init_welcome_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Welcome to the Web Security Toolkit")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        sqli_button = QPushButton("SQLi Detector")
        sqli_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.sqli_page))

        password_button = QPushButton("Password Strength Checker")
        password_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.password_page))

        encryption_button = QPushButton("Encryption Tool")
        encryption_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.encryption_page))

        layout.addWidget(title)
        layout.addSpacing(50)
        
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.addWidget(sqli_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(password_button)
        button_layout.addSpacing(20)
        button_layout.addWidget(encryption_button)

        layout.addLayout(button_layout)
        self.welcome_page.setLayout(layout)

    def init_sqli_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("SQLi Detector")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        self.sqli_input = QLineEdit()
        self.sqli_input.setPlaceholderText("Enter text to check for SQLi...")
        self.sqli_result = QLabel("")

        check_button = QPushButton("Check")
        check_button.clicked.connect(self.check_sqli)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.welcome_page))

        layout.addWidget(title)
        layout.addSpacing(50)
        layout.addWidget(self.sqli_input)
        layout.addSpacing(20)
        layout.addWidget(check_button)
        layout.addSpacing(20)
        layout.addWidget(self.sqli_result)
        layout.addStretch()
        layout.addWidget(back_button)

        self.sqli_page.setLayout(layout)

    def check_sqli(self):
        text = self.sqli_input.text()
        try:
            r = requests.post(f"{API_BASE}/detect_sqli", json={"text": text})
            r.raise_for_status()  # Raise an exception for bad status codes
            data = r.json()
            if data["vulnerable"]:
                self.sqli_result.setText("⚠️ SQLi Detected!")
            else:
                self.sqli_result.setText("✔️ Safe Input")
        except requests.exceptions.RequestException:
            self.sqli_result.setText("Error: Connection to the backend server failed. Please ensure the server is running.")

    def check_password(self):
        password = self.password_input.text()
        try:
            r = requests.post(f"{API_BASE}/check_password", json={"password": password})
            r.raise_for_status()  # Raise an exception for bad status codes
            data = r.json()
            self.password_result.setText(f"Strength: {data['strength']}")
        except requests.exceptions.RequestException:
            self.password_result.setText("Error: Connection to the backend server failed. Please ensure the server is running.")

    def init_encryption_page(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Encryption/Decryption Tool")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        # Algorithm Selection
        self.algo_combo = QComboBox()
        self.algo_combo.addItems(["Caesar", "Vigenere"])
        self.algo_combo.setStyleSheet("""
            QComboBox {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
                background-color: #34495e;
                color: #ecf0f1;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        
        # Mode Selection
        mode_layout = QHBoxLayout()
        self.encrypt_radio = QRadioButton("Encrypt")
        self.decrypt_radio = QRadioButton("Decrypt")
        self.encrypt_radio.setChecked(True)
        self.encrypt_radio.setStyleSheet("font-size: 16px;")
        self.decrypt_radio.setStyleSheet("font-size: 16px;")
        
        self.mode_group = QButtonGroup()
        self.mode_group.addButton(self.encrypt_radio)
        self.mode_group.addButton(self.decrypt_radio)
        
        mode_layout.addWidget(self.encrypt_radio)
        mode_layout.addWidget(self.decrypt_radio)
        mode_layout.setAlignment(Qt.AlignCenter)

        # Inputs
        self.cipher_input = QTextEdit()
        self.cipher_input.setPlaceholderText("Enter text...")
        self.cipher_input.setFixedHeight(100)
        self.cipher_input.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
                background-color: #34495e;
                color: #ecf0f1;
            }
        """)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Enter Shift (int) or Key (str)")

        self.cipher_result = QTextEdit()
        self.cipher_result.setReadOnly(True)
        self.cipher_result.setPlaceholderText("Result will appear here...")
        self.cipher_result.setFixedHeight(100)
        self.cipher_result.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 16px;
                background-color: #2c3e50;
                color: #ecf0f1;
            }
        """)

        run_button = QPushButton("Execute")
        run_button.clicked.connect(self.run_cipher)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.welcome_page))

        # Add to layout
        layout.addWidget(title)
        layout.addSpacing(30)
        layout.addWidget(QLabel("Algorithm:"))
        layout.addWidget(self.algo_combo)
        layout.addSpacing(10)
        layout.addLayout(mode_layout)
        layout.addSpacing(10)
        layout.addWidget(self.cipher_input)
        layout.addSpacing(10)
        layout.addWidget(self.key_input)
        layout.addSpacing(20)
        layout.addWidget(run_button)
        layout.addSpacing(20)
        layout.addWidget(self.cipher_result)
        layout.addStretch()
        layout.addWidget(back_button)

        self.encryption_page.setLayout(layout)

    def run_cipher(self):
        text = self.cipher_input.toPlainText()
        key_val = self.key_input.text()
        algo = self.algo_combo.currentText()
        mode = "encrypt" if self.encrypt_radio.isChecked() else "decrypt"
        
        payload = {
            "text": text,
            "algorithm": algo,
            "mode": mode
        }

        if algo == "Caesar":
            if not key_val.lstrip('-').isdigit():
                self.cipher_result.setPlainText("Error: Shift must be an integer for Caesar cipher.")
                return
            payload["shift"] = int(key_val)
        else:
            payload["key"] = key_val

        try:
            r = requests.post(f"{API_BASE}/cipher", json=payload)
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                 self.cipher_result.setPlainText(f"Error: {data['error']}")
            else:
                 self.cipher_result.setPlainText(data["result"])
        except requests.exceptions.RequestException as e:
            self.cipher_result.setPlainText(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RedesignedApp()
    window.show()
    sys.exit(app.exec_())
