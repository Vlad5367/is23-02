import sys
import json
import random
import time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QDialog, \
    QGridLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QFont


class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize quotes
        self.work_quotes = [
            "Отличная работа! Еще немного, и заслуженный отдых.",
            "Ты справляешься отлично! Скоро перерыв.",
            "Так держать! Осталось немного до отдыха.",
            "Прекрасный темп! Через пару минут можно будет отдохнуть.",
            "Молодец! Уже почти время для короткого перерыва.",
            "Ты на высоте! Скоро можешь расслабиться.",
            "У тебя прекрасно получается! Еще немного, и перерыв.",
            "Супер! Еще чуть-чуть, и заслуженный отдых.",
            "Ты справляешься великолепно! Скоро отдых.",
            "Отличный прогресс! Через несколько минут можно отдохнуть.",
            "Ты просто молодец! Скоро время для передышки.",
            "Ты делаешь большие успехи! Перерыв уже близко.",
            "Продолжай в том же духе! Через пару минут можно будет отдохнуть.",
            "Ты великолепен! Еще немного, и заслуженный перерыв."
        ]

        self.break_quotes = [
            "Отдыхай и наслаждайся моментом, заслуженный перерыв.",
            "Время для отдыха и восстановления энергии. Наслаждайся этим временем.",
            "Прекрасная работа! Приятно отдохнуть после продуктивного сеанса.",
            "Отлично справился! Наслаждайся перерывом и зарядись новой энергией.",
            "Время отдохнуть и расслабиться. Наслаждайся этим временем для себя.",
            "Приятного перерыва! Это заслуженный отдых после трудного труда.",
            "Отличная работа! Наслаждайся этим временем для отдыха и восстановления.",
            "Приятно расслабиться после успешного сеанса. Наслаждайся этим моментом.",
            "Отдыхай и наслаждайся этим моментом спокойствия после усердной работы.",
            "Отличная работа! Позволь себе отдохнуть и зарядиться новой энергией.",
            "Время насладиться моментом и отдохнуть. Ты этого заслужил.",
            "Приятного перерыва! Это время для расслабления и восстановления сил.",
            "Отдыхай и наслаждайся моментом покоя после продуктивного труда.",
            "Великолепная работа! Наслаждайся этим временем для отдыха и восстановления энергии."
        ]

        # Initialize achievements before loading them
        self.achievements = {
            "work_sessions": 0,
            "breaks": 0,
            "completed_sessions": 0
        }
        self.load_achievements()

        # Initialize UI and other components
        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.is_work_session = True

    def initUI(self):
        self.setWindowTitle('Помодоро Таймер')
        self.setGeometry(100, 100, 1000, 800)

        main_layout = QVBoxLayout()

        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Помодоро Таймер", self)
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)

        subtitle = QLabel("Учись эффективно: каждый помидор – шаг к успеху с Study Organizer", self)
        subtitle.setFont(QFont('Arial', 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        main_layout.addLayout(header_layout)

        # Timer buttons
        timer_buttons_layout = QHBoxLayout()

        self.start_1h_button = QPushButton('+ таймер на 1 час', self)
        self.start_1h_button.setStyleSheet("""
            QPushButton {
                background-color: #52CC7A;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45b367;
            }
        """)
        self.start_1h_button.clicked.connect(lambda: self.start_timer(1))
        timer_buttons_layout.addWidget(self.start_1h_button)

        self.start_2h_button = QPushButton('+ таймер на 2 часа', self)
        self.start_2h_button.setStyleSheet("""
            QPushButton {
                background-color: #52CC7A;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45b367;
            }
        """)
        self.start_2h_button.clicked.connect(lambda: self.start_timer(2))
        timer_buttons_layout.addWidget(self.start_2h_button)

        self.start_4h_button = QPushButton('+ таймер на 4 часа', self)
        self.start_4h_button.setStyleSheet("""
            QPushButton {
                background-color: #52CC7A;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45b367;
            }
        """)
        self.start_4h_button.clicked.connect(lambda: self.start_timer(4))
        timer_buttons_layout.addWidget(self.start_4h_button)

        main_layout.addLayout(timer_buttons_layout)

        # Main content
        content_layout = QHBoxLayout()

        # Circle icon
        self.circle_icon = QLabel(self)
        self.update_circle_icon('idle')  # Start with idle icon
        content_layout.addWidget(self.circle_icon)

        # Session information
        session_info_layout = QVBoxLayout()

        self.motivation_label = QLabel("Выбери таймер и начни учебу вместе со Study Organizer", self)
        self.motivation_label.setFont(QFont('Arial', 16))
        self.motivation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        session_info_layout.addWidget(self.motivation_label)

        self.time_label = QLabel("Время работы: 0:00\nДо перерыва: 0:00\nВсего осталось: 0:00", self)
        self.time_label.setFont(QFont('Arial', 16))
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        session_info_layout.addWidget(self.time_label)

        self.finish_button = QPushButton('завершить', self)
        self.finish_button.setStyleSheet("""
            QPushButton {
                background-color: #52CC7A;
                color: white;
                border-radius: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45b367;
            }
        """)
        self.finish_button.clicked.connect(self.confirm_finish_session)
        session_info_layout.addWidget(self.finish_button)

        content_layout.addLayout(session_info_layout)

        main_layout.addLayout(content_layout)

        # Achievements
        achievements_layout = QVBoxLayout()
        achievements_label = QLabel("Достижения", self)
        achievements_label.setFont(QFont('Arial', 18))
        achievements_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        achievements_layout.addWidget(achievements_label)

        icons_layout = QGridLayout()
        icons_layout.setSpacing(20)  # Add spacing for better alignment

        self.work_icon = QLabel(self)
        self.work_icon.setPixmap(QPixmap('work_icon.png').scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        icons_layout.addWidget(self.work_icon, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.break_icon = QLabel(self)
        self.break_icon.setPixmap(QPixmap('break_icon.png').scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        icons_layout.addWidget(self.break_icon, 0, 1, Qt.AlignmentFlag.AlignCenter)

        self.complete_icon = QLabel(self)
        self.complete_icon.setPixmap(QPixmap('complete_icon.png').scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio))
        icons_layout.addWidget(self.complete_icon, 0, 2, Qt.AlignmentFlag.AlignCenter)

        achievements_layout.addLayout(icons_layout)

        achievements_values_layout = QHBoxLayout()
        self.work_sessions_label = QLabel(f"{self.achievements['work_sessions']}", self)
        self.work_sessions_label.setFont(QFont('Arial', 16))
        self.work_sessions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        achievements_values_layout.addWidget(self.work_sessions_label)

        self.breaks_label = QLabel(f"{self.achievements['breaks']}", self)
        self.breaks_label.setFont(QFont('Arial', 16))
        self.breaks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        achievements_values_layout.addWidget(self.breaks_label)

        self.completed_sessions_label = QLabel(f"{self.achievements['completed_sessions']}", self)
        self.completed_sessions_label.setFont(QFont('Arial', 16))
        self.completed_sessions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        achievements_values_layout.addWidget(self.completed_sessions_label)

        achievements_layout.addLayout(achievements_values_layout)
        main_layout.addLayout(achievements_layout)

        # Help button
        self.help_button = QPushButton('?', self)
        self.help_button.setStyleSheet("""
            QPushButton {
                background-color: #52CC7A;
                color: white;
                border-radius: 15px;
                padding: 8px 13px;
            }
            QPushButton:hover {
                background-color: #45b367;
            }
        """)
        self.help_button.setMaximumWidth(30)
        self.help_button.clicked.connect(self.show_help)
        main_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)
        self.show()

    def update_circle_icon(self, state):
        if state == 'work':
            self.circle_icon.setPixmap(QPixmap('work_icon.png').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        elif state == 'rest':
            self.circle_icon.setPixmap(QPixmap('break_icon.png').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        elif state == 'complete':
            self.circle_icon.setPixmap(
                QPixmap('complete_icon.png').scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.circle_icon.setPixmap(QPixmap('idle_icon.png').scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))

    def start_timer(self, hours):
        self.work_time = hours * 60 * 60
        self.remaining_time = 25 * 60  # 25 minutes work period
        self.is_work_session = True
        self.update_circle_icon('work')
        self.motivation_label.setText(random.choice(self.work_quotes))
        self.timer.start(1000)

    def update_timer(self):
        self.remaining_time -= 1
        hours_left = int(self.work_time // 3600)
        minutes_left = int((self.work_time % 3600) // 60)
        self.time_label.setText(
            f"Время работы: {hours_left}:{minutes_left:02d}\nДо перерыва: {self.remaining_time // 60}:{self.remaining_time % 60:02d}\nВсего осталось: {hours_left}:{minutes_left:02d}"
        )
        self.work_time -= 1

        if self.remaining_time <= 0:
            if self.is_work_session:
                self.achievements['work_sessions'] += 1
                self.remaining_time = 5 * 60  # 5 minutes break
                self.is_work_session = False
                self.update_circle_icon('rest')
                self.motivation_label.setText(random.choice(self.break_quotes))
            else:
                self.achievements['breaks'] += 1
                self.remaining_time = 25 * 60  # 25 minutes work period
                self.is_work_session = True
                self.update_circle_icon('work')
                self.motivation_label.setText(random.choice(self.work_quotes))

        self.work_sessions_label.setText(f"{self.achievements['work_sessions']}")
        self.breaks_label.setText(f"{self.achievements['breaks']}")
        self.completed_sessions_label.setText(f"{self.achievements['completed_sessions']}")

    def confirm_finish_session(self):
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setWindowTitle("Подтверждение")
        confirm_dialog.setText("Вы уверены, что хотите завершить текущую сессию?")
        confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        confirm_dialog.setIcon(QMessageBox.Icon.Question)

        result = confirm_dialog.exec()
        if result == QMessageBox.StandardButton.Yes:
            self.finish_session()

    def finish_session(self):
        self.timer.stop()
        self.achievements['completed_sessions'] += 1
        self.work_sessions_label.setText(f"{self.achievements['work_sessions']}")
        self.breaks_label.setText(f"{self.achievements['breaks']}")
        self.completed_sessions_label.setText(f"{self.achievements['completed_sessions']}")
        self.update_circle_icon('complete')
        self.motivation_label.setText("Сессия завершена! Отличная работа!")
        self.time_label.setText(
            f"Время работы: {int(self.work_time // 60)}:00\nДо перерыва: 0:00\nВсего осталось: {int(self.work_time // 60)}:00"
        )

    def show_help(self):
        help_dialog = QDialog(self)
        help_dialog.setWindowTitle("Помощь")
        help_dialog.setGeometry(100, 100, 400, 300)

        help_layout = QVBoxLayout()
        help_text = QLabel(
            "Добро пожаловать в приложение 'Помодоро Таймер'! Вот как вы можете его использовать:\n\n"
            "1. Выберите продолжительность таймера (1 час, 2 часа или 4 часа) для начала работы.\n"
            "2. Следуйте циклу работы и перерывов: 25 минут работы и 5 минут перерыва.\n"
            "3. Используйте кнопку 'завершить', чтобы завершить текущую сессию и сохранить достижения.\n"
            "4. Просматривайте свои достижения в разделе 'Достижения'.\n\n"
            "Наслаждайтесь эффективной работой и учёбой!"
        )
        help_layout.addWidget(help_text)

        close_button = QPushButton("Закрыть", help_dialog)
        close_button.clicked.connect(help_dialog.close)
        help_layout.addWidget(close_button)

        help_dialog.setLayout(help_layout)
        help_dialog.exec()

    def closeEvent(self, event):
        self.save_achievements()
        event.accept()

    def load_achievements(self):
        try:
            with open("achievements.json", "r") as file:
                self.achievements = json.load(file)
        except FileNotFoundError:
            pass

    def save_achievements(self):
        with open("achievements.json", "w") as file:
            json.dump(self.achievements, file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PomodoroTimer()
    sys.exit(app.exec())
