import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout, QTextEdit, QPlainTextEdit
from PyQt5.QtGui import QFont
from register import register_to_csv
import time
import json
import os
from PyQt5.QtWidgets import QDateEdit, QCalendarWidget
from PyQt5.QtCore import QDate

class Chronometer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chronometer")
        self.setGeometry(200, 200, 600, 300)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.create_input_page()

    def create_input_page(self):
        self.hourly_rate_label = QLabel("Enter hourly rate:")
        self.hourly_rate_input = QLineEdit()

        self.date_label = QLabel("Enter date (YYYY-MM-DD):")
        self.date_input = QDateEdit(self)
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.set_hourly_rate_button = QPushButton("Set hourly rate")
        self.set_hourly_rate_button.clicked.connect(self.set_hourly_rate)
        self.see_saves_button = QPushButton("See saves")
        self.see_saves_button.clicked.connect(self.see_saves)
        self.data_menu_button = QPushButton("Data Menu")
        self.data_menu_button.clicked.connect(self.open_data_menu)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.hourly_rate_label, 0, 0)
        grid_layout.addWidget(self.hourly_rate_input, 0, 1)
        grid_layout.addWidget(self.date_label, 1, 0)
        grid_layout.addWidget(self.date_input, 1, 1)
        grid_layout.addWidget(self.set_hourly_rate_button, 2, 0)
        grid_layout.addWidget(self.see_saves_button, 2, 1)
        grid_layout.addWidget(self.data_menu_button, 3, 0, 1, 2)

        self.layout.addLayout(grid_layout)


    def set_hourly_rate(self):
        try:
            self.hourly_rate_value = float(self.hourly_rate_input.text())
            self.date_value = self.date_input.text()
            self.hourly_rate_label.hide()
            self.hourly_rate_input.hide()
            self.date_label.hide()
            self.date_input.hide()
            self.set_hourly_rate_button.hide()
            self.see_saves_button.hide()
            self.create_chronometer()
        except ValueError:
            self.hourly_rate_label.setText("Invalid hourly rate. Please enter a number.")

    def register_to_csv(self):
        register_to_csv()

    def open_data_menu(self):
        self.data_menu_window = QWidget()
        self.data_menu_window.setWindowTitle("Data Menu")
        self.data_menu_window.setGeometry(200, 200, 200, 100)

        self.register_to_csv_button = QPushButton("Register to CSV", self.data_menu_window)
        self.register_to_csv_button.clicked.connect(self.register_to_csv)
        self.register_to_csv_button.move(20, 20)
        self.data_menu_window.show()

    def create_chronometer(self):
        self.pay_label = QLabel("Total pay: $0.00")
        self.pay_label.setFont(QFont("Helvetica", 24))
        self.pay_label.move(200, 50)
        self.layout.addWidget(self.pay_label)

        self.time_label = QLabel("00:00:00")
        self.time_label.setFont(QFont("Helvetica", 48))
        self.time_label.move(200, 100)
        self.layout.addWidget(self.time_label)

        self.seconds = 0
        self.running = False
        self.paused = False

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start)
        self.start_button.move(100, 200)
        self.layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause)
        self.pause_button.move(200, 200)
        self.layout.addWidget(self.pause_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)
        self.save_button.move(300, 200)
        self.layout.addWidget(self.save_button)

    def start(self):
        if not self.running:
            self.running = True
            self.start_button.setText("Reset")
            self.start_button.clicked.disconnect()
            self.start_button.clicked.connect(self.reset)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.increment_time)
            self.timer.start(1000)

    def pause(self):
        if self.running:
            self.paused = True
            self.timer.stop()
            self.pause_button.setText("Resume")
            self.pause_button.clicked.disconnect()
            self.pause_button.clicked.connect(self.resume)

    def resume(self):
        self.paused = False
        self.timer.start(1000)
        self.pause_button.setText("Pause")
        self.pause_button.clicked.disconnect()
        self.pause_button.clicked.connect(self.pause)

    def reset(self):
        self.running = False
        self.paused = False
        self.seconds = 0
        self.time_label.setText("00:00:00")
        self.pay_label.setText("Total pay: $0.00")
        self.start_button.setText("Start")
        self.start_button.clicked.disconnect()
        self.start_button.clicked.connect(self.start)

    def increment_time(self):
        if self.running and not self.paused:
            self.seconds += 1
            self.time_label.setText(time.strftime("%H:%M:%S", time.gmtime(self.seconds)))
            self.pay_label.setText(f"Total pay: ${self.hourly_rate_value * self.seconds / 3600:.2f}")

    def save(self):
        data = {
            'hourly_rate': self.hourly_rate_value,
            'time': self.time_label.text(),
            'pay': float(self.pay_label.text().split('$')[1])
        }

        if os.path.exists('../data/saves.json'):
            with open('../data/saves.json', 'r') as file:
                saves = json.load(file)
                if self.date_value in saves:
                    saves[self.date_value].append(data)
                else:
                    saves[self.date_value] = [data]
            with open('../data/saves.json', 'w') as file:
                json.dump(saves, file, indent=4)
        else:
            with open('../data/saves.json', 'w') as file:
                json.dump({self.date_value: [data]}, file, indent=4)

    # Page that displays the content of saves.json
    def see_saves(self):
        self.hourly_rate_label.hide()
        self.hourly_rate_input.hide()
        self.date_label.hide()
        self.date_input.hide()
        self.set_hourly_rate_button.hide()
        self.see_saves_button.hide()
        self.data_menu_button.hide()

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        self.layout.addWidget(back_button)

        # Reading from saves.json
        try:
            with open('clock/data/saves.json', 'r') as file:
                saves = json.load(file)
                plain_text_edit = QPlainTextEdit()
                plain_text_edit.setPlainText(json.dumps(saves, indent=4))
                self.layout.addWidget(plain_text_edit)
        except FileNotFoundError:
            print("saves.json file not found")
        except json.JSONDecodeError:
            print("Error parsing saves.json file")

    # Go Back button
    def go_back(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        self.create_input_page()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chronometer = Chronometer()
    chronometer.show()
    sys.exit(app.exec_())