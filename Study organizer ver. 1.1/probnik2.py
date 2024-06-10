import random
import sys
import json
from datetime import datetime

from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
                             QStackedWidget, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QFileDialog, QDialog,
                             QDialogButtonBox, QMessageBox, QGridLayout, QScrollArea, QDateTimeEdit, QFormLayout,
                             QComboBox, QMenu, QCalendarWidget)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QPoint, pyqtSignal, QDateTime, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap, QAction

class CalendarWidget(QWidget):
    def init(self):
        super().init()
        self.notes = {}
        self.load_notes()
        self.initUI()

    def initUI(self):
        Calendar_layout = QVBoxLayout()

        # Добавление кнопок переключения вида
        self.view_selector = QComboBox()
        self.view_selector.addItems(["Месяц", "Неделя"])
        self.view_selector.currentIndexChanged.connect(self.change_view)
        Calendar_layout.addWidget(self.view_selector)

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_note)
        Calendar_layout.addWidget(self.calendar)

        self.note_area = QTextEdit()
        Calendar_layout.addWidget(self.note_area)

        self.save_button = QPushButton("Сохранить заметку")
        self.save_button.clicked.connect(self.save_note)
        Calendar_layout.addWidget(self.save_button)

        self.setLayout(Calendar_layout)

    def change_view(self):
        if self.view_selector.currentText() == "Месяц":
            self.calendar.setGridVisible(True)
        else:
            self.calendar.setGridVisible(False)

    def show_note(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.note_area.setText(self.notes.get(date, ""))

    def save_note(self):
        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.notes[date] = self.note_area.toPlainText()
        self.save_notes()

    def save_notes(self):
        with open("notes.json", "w", encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=4)

    def load_notes(self):
        try:
            with open("notes.json", "r", encoding='utf-8') as f:
                self.notes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.notes = {}

class TaskCard(QWidget):
    def __init__(self, title, deadline, task_name, subject):
        super().__init__()
        self.initUI(title, deadline, task_name, subject)

    def initUI(self, title, deadline, task_name, subject):
        Task_layout = QVBoxLayout()

        self.titleLabel = QLabel(title)
        self.deadlineLabel = QLabel(deadline)
        self.taskNameLabel = QLabel(task_name)
        self.subjectLabel = QLabel(subject)

        menuButton = QPushButton("...")
        menuButton.setFixedSize(30, 30)
        menuButton.clicked.connect(self.showMenu)

        Task_layout.addWidget(self.titleLabel)
        Task_layout.addWidget(self.deadlineLabel)
        Task_layout.addWidget(self.taskNameLabel)
        Task_layout.addWidget(self.subjectLabel)
        Task_layout.addWidget(menuButton)

        self.setLayout(Task_layout)
        self.setStyleSheet("background-color: #E4E4E2; border-radius: 10px; padding: 10px;")

    def showMenu(self):
        menu = QMenu(self)
        editAction = QAction('Edit', self)
        deleteAction = QAction('Delete', self)
        archiveAction = QAction('Archive', self)

        menu.addAction(editAction)
        menu.addAction(deleteAction)
        menu.addAction(archiveAction)

        editAction.triggered.connect(self.editTask)
        deleteAction.triggered.connect(self.deleteTask)
        archiveAction.triggered.connect(self.archiveTask)

        menu.exec(self.mapToGlobal(self.sender().pos()))

    def editTask(self):
        dialog = AddTaskDialog()
        dialog.titleEdit.setText(self.titleLabel.text())
        dialog.deadlineEdit.setDateTime(datetime.strptime(self.deadlineLabel.text(), '%d.%m.%Y'))
        dialog.taskNameEdit.setText(self.taskNameLabel.text())
        dialog.subjectEdit.setText(self.subjectLabel.text())
        current_category = "Задачи" if self.parentWidget() == window.tasksLayout else "В процессе"
        dialog.categoryComboBox.setCurrentText(current_category)

        if dialog.exec():
            title, deadline, task_name, subject, category = dialog.getTaskData()
            self.titleLabel.setText(title)
            self.deadlineLabel.setText(deadline)
            self.taskNameLabel.setText(task_name)
            self.subjectLabel.setText(subject)

            if category != current_category:
                self.setParent(None)  # Remove from the current layout
                if category == "В процессе":
                    window.inProgressLayout.addWidget(self)
                else:
                    window.tasksLayout.addWidget(self)

            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, MainWindow):
                    widget.saveTasks()
                    break

    def deleteTask(self):
        self.setParent(None)

    def archiveTask(self):
        self.setParent(None)
        window.archiveWindow.addArchivedTask(self)
        window.saveTasks()


class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить задание')
        self.setGeometry(100, 100, 300, 300)

        Task_layout = QFormLayout()

        self.titleEdit = QLineEdit()
        self.deadlineEdit = QDateTimeEdit(calendarPopup=True)
        self.deadlineEdit.setDateTime(datetime.now())
        self.taskNameEdit = QLineEdit()
        self.subjectEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(["Задачи", "В процессе"])

        Task_layout.addRow('Название:', self.titleEdit)
        Task_layout.addRow('Дедлайн:', self.deadlineEdit)
        Task_layout.addRow('Название работы:', self.taskNameEdit)
        Task_layout.addRow('Предмет:', self.subjectEdit)
        Task_layout.addRow('Категория:', self.categoryComboBox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)

        Task_layout.addWidget(buttons)
        self.setLayout(Task_layout)

    def validate(self):
        if not self.titleEdit.text() or not self.deadlineEdit.text() or not self.taskNameEdit.text() or not self.subjectEdit.text():
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
        else:
            self.accept()

    def getTaskData(self):
        return (
            self.titleEdit.text(),
            self.deadlineEdit.dateTime().toString('dd.MM.yyyy'),
            self.taskNameEdit.text(),
            self.subjectEdit.text(),
            self.categoryComboBox.currentText()
        )


class ArchiveWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Архив')
        self.setGeometry(100, 100, 800, 600)

        TaskWidget = QWidget()
        Task_layout = QVBoxLayout()

        tasksColumn = QVBoxLayout()
        tasksTitle = QLabel("Архив")
        tasksScroll = QScrollArea()
        tasksWidget = QWidget()
        self.tasksLayout = QVBoxLayout()

        tasksWidget.setLayout(self.tasksLayout)
        tasksScroll.setWidget(tasksWidget)
        tasksScroll.setWidgetResizable(True)

        tasksColumn.addWidget(tasksTitle)
        tasksColumn.addWidget(tasksScroll)

        Task_layout.addLayout(tasksColumn)

        TaskWidget.setLayout(Task_layout)
        self.setCentralWidget(TaskWidget)

    def addArchivedTask(self, task):
        self.tasksLayout.addWidget(task)


class Deadlines(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.archiveWindow = ArchiveWindow()
        self.loadTasks()
        self.initTimer()

    def initUI(self):
        self.setWindowTitle('Задачи и дедлайны')
        self.setGeometry(100, 100, 1024, 768)

        TaskWidget = QWidget()
        mainLayout = QVBoxLayout()

        headerLayout = QHBoxLayout()

        titleLabel = QLabel("Задачи и дедлайны")
        descriptionLabel = QLabel("Сделай каждый дедлайн достижимым. Управляй задачами с умом в Study Organizer.")

        headerRightLayout = QVBoxLayout()
        addButton = QPushButton("Добавить")
        addButton.setStyleSheet("background-color: #82D19C; border-radius: 10px;")
        addButton.clicked.connect(self.showAddTaskDialog)
        archiveButton = QPushButton("Архив")
        archiveButton.setStyleSheet("background-color: #82D19C; border-radius: 10px;")
        archiveButton.clicked.connect(self.showArchive)

        headerRightLayout.addWidget(addButton)
        headerRightLayout.addWidget(archiveButton)

        headerLayout.addWidget(titleLabel)
        headerLayout.addWidget(descriptionLabel)
        headerLayout.addLayout(headerRightLayout)

        mainLayout.addLayout(headerLayout)

        contentLayout = QHBoxLayout()

        tasksColumn = QVBoxLayout()
        tasksTitle = QLabel("Задачи")
        tasksScroll = QScrollArea()
        tasksWidget = QWidget()
        self.tasksLayout = QVBoxLayout()

        tasksWidget.setLayout(self.tasksLayout)
        tasksScroll.setWidget(tasksWidget)
        tasksScroll.setWidgetResizable(True)

        tasksColumn.addWidget(tasksTitle)
        tasksColumn.addWidget(tasksScroll)

        inProgressColumn = QVBoxLayout()
        inProgressTitle = QLabel("В процессе")
        inProgressScroll = QScrollArea()
        inProgressWidget = QWidget()
        self.inProgressLayout = QVBoxLayout()

        inProgressWidget.setLayout(self.inProgressLayout)
        inProgressScroll.setWidget(inProgressWidget)
        inProgressScroll.setWidgetResizable(True)

        inProgressColumn.addWidget(inProgressTitle)
        inProgressColumn.addWidget(inProgressScroll)

        contentLayout.addLayout(tasksColumn)
        contentLayout.addLayout(inProgressColumn)

        mainLayout.addLayout(contentLayout)

        TaskWidget.setLayout(mainLayout)
        self.setCentralWidget(TaskWidget)

    def showAddTaskDialog(self):
        dialog = AddTaskDialog()
        if dialog.exec():
            title, deadline, task_name, subject, category = dialog.getTaskData()
            task = TaskCard(title, deadline, task_name, subject)
            if category == "Задачи":
                self.tasksLayout.addWidget(task)
            else:
                self.inProgressLayout.addWidget(task)
            self.saveTasks()

    def showArchive(self):
        self.archiveWindow.show()

    def archiveTask(self, task):
        self.archiveWindow.addArchivedTask(task)
        self.saveTasks()

    def saveTasks(self):
        tasks = []
        in_progress = []
        archived = []

        for i in range(self.tasksLayout.count()):
            task = self.tasksLayout.itemAt(i).widget()
            if task:
                tasks.append({
                    "title": task.titleLabel.text(),
                    "deadline": task.deadlineLabel.text(),
                    "task_name": task.taskNameLabel.text(),
                    "subject": task.subjectLabel.text()
                })

        for i in range(self.inProgressLayout.count()):
            task = self.inProgressLayout.itemAt(i).widget()
            if task:
                in_progress.append({
                    "title": task.titleLabel.text(),
                    "deadline": task.deadlineLabel.text(),
                    "task_name": task.taskNameLabel.text(),
                    "subject": task.subjectLabel.text()
                })

        for i in range(self.archiveWindow.tasksLayout.count()):
            task = self.archiveWindow.tasksLayout.itemAt(i).widget()
            if task:
                archived.append({
                    "title": task.titleLabel.text(),
                    "deadline": task.deadlineLabel.text(),
                    "task_name": task.taskNameLabel.text(),
                    "subject": task.subjectLabel.text()
                })

        with open('tasks.json', 'w') as file:
            json.dump({
                "tasks": tasks,
                "in_progress": in_progress,
                "archived": archived
            }, file)

    def loadTasks(self):
        try:
            with open('tasks.json', 'r') as file:
                data = json.load(file)
                for task_data in data.get("tasks", []):
                    task = TaskCard(task_data["title"], task_data["deadline"], task_data["task_name"], task_data["subject"])
                    self.tasksLayout.addWidget(task)

                for task_data in data.get("in_progress", []):
                    task = TaskCard(task_data["title"], task_data["deadline"], task_data["task_name"], task_data["subject"])
                    self.inProgressLayout.addWidget(task)

                for task_data in data.get("archived", []):
                    task = TaskCard(task_data["title"], task_data["deadline"], task_data["task_name"], task_data["subject"])
                    self.archiveWindow.addArchivedTask(task)
        except FileNotFoundError:
            pass

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.checkDeadlines)
        self.timer.start(60000)  # Check every minute

    def checkDeadlines(self):
        now = datetime.now()
        for i in range(self.tasksLayout.count()):
            task = self.tasksLayout.itemAt(i).widget()
            if task:
                deadline = datetime.strptime(task.deadlineLabel.text(), '%d.%m.%Y')
                if deadline < now:
                    task.setStyleSheet("background-color: red;")
                else:
                    task.setStyleSheet("background-color: #E4E4E2;")

        for i in range(self.inProgressLayout.count()):
            task = self.inProgressLayout.itemAt(i).widget()
            if task:
                deadline = datetime.strptime(task.deadlineLabel.text(), '%d.%m.%Y')
                if deadline < now:
                    task.setStyleSheet("background-color: red;")
                else:
                    task.setStyleSheet("background-color: #E4E4E2;")

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

        timer_layout = QVBoxLayout()

        # Header
        header_layout = QVBoxLayout()
        title = QLabel("Помодоро Таймер🍅", self)
        title.setFont(QFont('Arial', 24))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)

        subtitle = QLabel("Учись эффективно: каждый помидор – шаг к успеху с Study Organizer", self)
        subtitle.setFont(QFont('Arial', 14))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        timer_layout.addLayout(header_layout)

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

        timer_layout.addLayout(timer_buttons_layout)

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

        timer_layout.addLayout(content_layout)

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
        timer_layout.addLayout(achievements_layout)

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
        timer_layout.addWidget(self.help_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(timer_layout)
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
        self.work_time = hours * 3600  # Часы в секунды
        self.remaining_time = 25 * 60  # 25 минут работы в секундах
        self.is_work_session = True
        self.update_circle_icon('work')
        self.motivation_label.setText(random.choice(self.work_quotes))
        self.timer.start(1000)

    def update_timer(self):
        self.remaining_time -= 1
        self.work_time -= 1

        if self.remaining_time <= 0:
            if self.is_work_session:
                self.achievements['work_sessions'] += 1
                self.remaining_time = 5 * 60  # 5 минут перерыв
                self.is_work_session = False
                self.update_circle_icon('rest')
                self.motivation_label.setText(random.choice(self.break_quotes))
            else:
                self.achievements['breaks'] += 1
                self.remaining_time = 25 * 60  # 25 минут работы
                self.is_work_session = True
                self.update_circle_icon('work')
                self.motivation_label.setText(random.choice(self.work_quotes))

            self.work_sessions_label.setText(f"{self.achievements['work_sessions']}")
            self.breaks_label.setText(f"{self.achievements['breaks']}")

        if self.work_time <= 0:
            self.timer.stop()
            self.achievements['completed_sessions'] += 1
            self.completed_sessions_label.setText(f"{self.achievements['completed_sessions']}")
            self.update_circle_icon('complete')
            self.motivation_label.setText("Поздравляем! Вы завершили сессию!")
            self.time_label.setText("Время работы: 0:00\nДо перерыва: 0:00\nВсего осталось: 0:00")
            self.save_achievements()

        hours_left = int(self.work_time // 3600)
        minutes_left = int((self.work_time % 3600) // 60)
        self.time_label.setText(
            f"Время работы: {hours_left}:{minutes_left:02d}\nДо перерыва: {self.remaining_time // 60}:{self.remaining_time % 60:02d}\nВсего осталось: {hours_left}:{minutes_left:02d}"
        )

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
        # Достижения не добавляются при ручном завершении
        self.update_circle_icon('idle.png')
        self.motivation_label.setText("Сессия завершена! Отличная работа!")
        self.time_label.setText("Время работы: 0:00\nДо перерыва: 0:00\nВсего осталось: 0:00")

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
            "Наслаждайтесь эффективной учёбой!"
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

class Note:
    def __init__(self, title, subtitle, description, image_path=None, favorite=False, date_created=None):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.image_path = image_path
        self.favorite = favorite
        self.date_created = date_created if date_created else QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm")

    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "description": self.description,
            "image_path": self.image_path,
            "favorite": self.favorite,
            "date_created": self.date_created
        }

    @staticmethod
    def from_dict(data):
        return Note(
            title=data["title"],
            subtitle=data["subtitle"],
            description=data["description"],
            image_path=data.get("image_path"),
            favorite=data.get("favorite", False),
            date_created=data.get("date_created")
        )

class NotesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = []
        self.initUI()

    def initUI(self):
        try:
            main_layout = QHBoxLayout(self)

            self.notes_list = QListWidget()
            self.notes_list.itemClicked.connect(self.display_note)
            main_layout.addWidget(self.notes_list)

            self.note_detail_widget = QWidget()
            self.note_detail_layout = QVBoxLayout(self.note_detail_widget)

            self.note_image = QLabel()
            self.note_image.setFixedSize(200, 200)
            self.note_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.note_detail_layout.addWidget(self.note_image)

            self.note_title_subtitle = QLabel()
            self.note_title_subtitle.setFont(QFont("Arial", 16))
            self.note_detail_layout.addWidget(self.note_title_subtitle)

            self.note_description = QTextEdit()
            self.note_description.setReadOnly(True)
            self.note_detail_layout.addWidget(self.note_description)

            self.delete_button = QPushButton("Удалить")
            self.delete_button.setFont(QFont("Arial", 12))
            self.delete_button.setStyleSheet("background-color: #82D19C; border-radius: 10px; padding: 10px;")
            self.delete_button.clicked.connect(self.delete_note)
            self.note_detail_layout.addWidget(self.delete_button)

            self.add_button = QPushButton("✍ Добавить")
            self.add_button.setFont(QFont("Arial", 12))
            self.add_button.setStyleSheet("background-color: #82D19C; border-radius: 10px; padding: 10px;")
            self.add_button.clicked.connect(self.add_note)
            self.note_detail_layout.addWidget(self.add_button)

            self.edit_button = QPushButton("Редактировать")
            self.edit_button.setFont(QFont("Arial", 12))
            self.edit_button.setStyleSheet("background-color: #82D19C; border-radius: 10px; padding: 10px;")
            self.edit_button.clicked.connect(self.edit_note)
            self.note_detail_layout.addWidget(self.edit_button)
            self.load_notes()
            main_layout.addWidget(self.note_detail_widget)
        except Exception as e:
            print(f"Error in NotesWidget.initUI: {e}")

    def delete_note(self):
        try:
            note_index = self.notes_list.currentRow()
            if note_index >= 0 and note_index < len(self.notes):
                del self.notes[note_index]
                self.update_notes_list()
                self.clear_note_details()
                self.save_notes()
        except Exception as e:
            print(f"Error in NotesWidget.delete_note: {e}")

    def clear_note_details(self):
        self.note_title_subtitle.setText("")
        self.note_description.clear()
        self.note_image.setPixmap(QPixmap())

    def toggle_favorite(self):
        try:
            note_index = self.notes_list.currentRow()
            if note_index >= 0 and note_index < len(self.notes):
                self.notes[note_index].favorite = not self.notes[note_index].favorite
                self.update_notes_list()
                self.save_notes()
        except Exception as e:
            print(f"Error in NotesWidget.toggle_favorite: {e}")

    def display_note(self, item):
        try:
            note = self.notes[self.notes_list.row(item)]
            self.note_title_subtitle.setText(f"{note.title}\n{note.subtitle}")
            self.note_description.setPlainText(note.description)
            if note.image_path:
                pixmap = QPixmap(note.image_path)
                self.note_image.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                self.note_image.setPixmap(QPixmap())
        except Exception as e:
            print(f"Ошибка: {e}")

    def edit_note(self):
        try:
            note_index = self.notes_list.currentRow()
            if note_index >= 0 and note_index < len(self.notes):
                note = self.notes[note_index]
                self.note_title_subtitle.setText(f"Edit: {note.title}")
                self.edit_note_dialog(note)
        except Exception as e:
            print(f"Ошибка: {e}")

    def add_note_to_list(self, note, index=None):
        try:
            item = QListWidgetItem()
            item.setSizeHint(QSize(400, 100))

            widget_item = QWidget()
            layout = QHBoxLayout(widget_item)

            image_label = QLabel()
            if note.image_path:
                pixmap = QPixmap(note.image_path)
                image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            else:
                image_label.setPixmap(
                    QPixmap("/mnt/data/image.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            image_label.setFixedSize(100, 100)
            layout.addWidget(image_label)

            text_layout = QVBoxLayout()
            title_label = QLabel(note.title)
            subtitle_label = QLabel(note.subtitle)
            title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            subtitle_label.setFont(QFont("Arial", 10))
            text_layout.addWidget(title_label)
            text_layout.addWidget(subtitle_label)

            layout.addLayout(text_layout)

            favorite_button = QPushButton("☆" if not note.favorite else "★")
            favorite_button.setCheckable(True)
            favorite_button.setChecked(note.favorite)
            favorite_button.clicked.connect(lambda checked, n=note: self.toggle_favorite_from_button(n, checked))
            layout.addWidget(favorite_button)

            widget_item.setLayout(layout)
            item.setSizeHint(widget_item.sizeHint())

            if index is not None:
                self.notes_list.insertItem(index, item)
            else:
                self.notes_list.addItem(item)
            self.notes_list.setItemWidget(item, widget_item)
        except Exception as e:
            print(f"Error in NotesWidget.add_note_to_list: {e}")

    def toggle_favorite_from_button(self, note, is_favorite):
        note.favorite = is_favorite
        self.update_notes_list()
        self.save_notes()

    def update_notes_list(self):
        try:
            self.notes_list.clear()
            self.notes.sort(key=lambda x: not x.favorite)
            for note in self.notes:
                self.add_note_to_list(note)
        except Exception as e:
            print(f"Error in NotesWidget.update_notes_list: {e}")

    def add_note(self):
        try:
            new_note = Note(
                title="Введите заголовок",
                subtitle="Введите подзаголовок",
                description="Введите описание"
            )
            self.notes.append(new_note)
            self.update_notes_list()
            self.edit_note_dialog(new_note)
        except Exception as e:
            print(f"Error in NotesWidget.add_note: {e}")

    def edit_note_dialog(self, note):
        try:
            dialog = NoteEditDialog(note, self)
            dialog.exec()
            self.update_notes_list()
            self.save_notes()
        except Exception as e:
            print(f"Error in NotesWidget.edit_note_dialog: {e}")

    def save_notes(self):
        try:
            notes_data = [note.to_dict() for note in self.notes]
            with open("notes.json", "w", encoding="utf-8") as f:
                json.dump(notes_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error in NotesWidget.save_notes: {e}")

    def load_notes(self):
        try:
            with open("notes.json", "r", encoding="utf-8") as f:
                notes_data = json.load(f)
                self.notes = [Note.from_dict(note) for note in notes_data]
                self.update_notes_list()
        except FileNotFoundError:
            self.notes = []
        except Exception as e:
            print(f"Error in NotesWidget.load_notes: {e}")


class NoteEditDialog(QDialog):
    def __init__(self, note, parent=None):
        super().__init__(parent)
        self.note = note
        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle("Редактировать заметку")
            layout = QVBoxLayout(self)

            self.title_edit = QLineEdit(self.note.title)
            self.title_edit.setPlaceholderText("Заголовок")
            layout.addWidget(self.title_edit)

            self.subtitle_edit = QLineEdit(self.note.subtitle)
            self.subtitle_edit.setPlaceholderText("Подзаголовок")
            layout.addWidget(self.subtitle_edit)

            self.description_edit = QTextEdit(self.note.description)
            self.description_edit.setPlaceholderText("Описание")
            layout.addWidget(self.description_edit)

            self.image_path_edit = QLineEdit(self.note.image_path if self.note.image_path else "")
            self.image_path_edit.setPlaceholderText("Путь к изображению")
            layout.addWidget(self.image_path_edit)

            self.image_button = QPushButton("Выбрать изображение")
            self.image_button.clicked.connect(self.select_image)
            layout.addWidget(self.image_button)

            buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(self.save_note)
            buttons.rejected.connect(self.reject)
            layout.addWidget(buttons)

            self.setLayout(layout)
        except Exception as e:
            print(f"Error in NoteEditDialog.initUI: {e}")

    def select_image(self):
        try:
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(self, "Выбрать изображение", "",
                                                       "Images (*.png *.xpm *.jpg *.bmp *.gif)")
            if file_path:
                self.image_path_edit.setText(file_path)
        except Exception as e:
            print(f"Error in NoteEditDialog.select_image: {e}")

    def save_note(self):
        try:
            self.note.title = self.title_edit.text()
            self.note.subtitle = self.subtitle_edit.text()
            self.note.description = self.description_edit.toPlainText()
            self.note.image_path = self.image_path_edit.text() if self.image_path_edit.text() else None
            self.accept()
        except Exception as e:
            print(f"Error in NoteEditDialog.save_note: {e}")

    def accept(self):
        try:
            self.note.title = self.title_edit.text()
            self.note.subtitle = self.subtitle_edit.text()
            self.note.description = self.description_edit.toPlainText()
            super().accept()
        except Exception as e:
            print(f"Error in NoteEditDialog.accept: {e}")

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        try:
            layout = QHBoxLayout(self)
            self.setFixedHeight(40)
            self.setStyleSheet("""
                background-color: #E0E0E0;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            """)

            self.title = QLabel("Study Organizer")
            self.title.setFont(QFont("Arial", 12))
            self.title.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignLeft)

            layout.addStretch()

            self.minimize_button = QPushButton("—")
            self.minimize_button.setFixedSize(40, 40)
            self.minimize_button.setStyleSheet("background-color: #82D19C; border: none;")
            self.minimize_button.clicked.connect(self.minimize_window)
            layout.addWidget(self.minimize_button, alignment=Qt.AlignmentFlag.AlignRight)

            self.maximize_button = QPushButton("☐")
            self.maximize_button.setFixedSize(40, 40)
            self.maximize_button.setStyleSheet("background-color: #82D19C; border: none;")
            self.maximize_button.clicked.connect(self.maximize_window)
            layout.addWidget(self.maximize_button, alignment=Qt.AlignmentFlag.AlignRight)

            self.close_button = QPushButton("✕")
            self.close_button.setFixedSize(40, 40)
            self.close_button.setStyleSheet("background-color: #FF6961; border: none;")
            self.close_button.clicked.connect(self.close_window)
            layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignRight)

            self.setLayout(layout)
        except Exception as e:
            print(f"Error in CustomTitleBar.initUI: {e}")

    def minimize_window(self):
        self.window().showMinimized()

    def maximize_window(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def close_window(self):
        self.window().close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressing = True
            self.start = self.mapToGlobal(event.pos())
            self.parentWidget().startPos = self.mapToGlobal(event.pos())
            self.window().startPos = self.window().frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.window().move(self.window().startPos + self.movement)
            self.start = self.mapToGlobal(event.pos())

    def mouseReleaseEvent(self, event):
        self.pressing = False

class MainWindow(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle('Study Organizer')
            self.setGeometry(100, 100, 1200, 800)
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

            central_widget = QWidget()
            self.setCentralWidget(central_widget)

            main_layout = QVBoxLayout(central_widget)

            self.title_bar = CustomTitleBar(self)
            main_layout.addWidget(self.title_bar)

            content_layout = QHBoxLayout()
            main_layout.addLayout(content_layout)

            logo_path = "your_logo.png"
            icons = {
                'Главная': 'icon_home.png',
                '   Цели': 'icon_goals.png',
                'Конспекты': 'icon_notes.png',
                'Календарь': 'icon_calendar.png',
                'Помодоро': 'icon_pomodoro.png'
            }
            self.side_panel = SidePanel(logo_path, icons)
            self.side_panel.buttonClicked.connect(self.changePage)
            content_layout.addWidget(self.side_panel)

            self.stack = QStackedWidget()
            self.pages = {
                'Главная': QWidget(),
                '   Цели': Deadlines(),
                'Конспекты': NotesWidget(),
                'Календарь': CalendarWidget(),
                'Помодоро': PomodoroTimer()
            }
            for page in self.pages.values():
                self.stack.addWidget(page)

            content_layout.addWidget(self.stack)
            self.changePage('home')
        except Exception as e:
            print(f"Error in MainWindow.__init__: {e}")

    def changePage(self, page_name):
        try:
            self.stack.setCurrentWidget(self.pages[page_name])
            self.side_panel.setActiveButton(page_name)
        except Exception as e:
            print(f"Error in MainWindow.changePage: {e}")

    def mousePressEvent(self, event):
        try:
            if event.button() == Qt.MouseButton.LeftButton:
                self.oldPos = event.globalPosition().toPoint()
        except Exception as e:
            print(f"Error in MainWindow.mousePressEvent: {e}")

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == Qt.MouseButton.LeftButton:
                delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPosition().toPoint()
        except Exception as e:
            print(f"Error in MainWindow.mouseMoveEvent: {e}")

class SidePanel(QWidget):
    buttonClicked = pyqtSignal(str)

    def __init__(self, logo_path, icons):
        try:
            super().__init__()
            self.logo_path = logo_path
            self.icons = icons
            self.initUI()
        except Exception as e:
            print(f"Error in SidePanel.__init__: {e}")

    def initUI(self):
        try:
            self.setFixedWidth(60)
            self.setStyleSheet("background-color: #E4E4E2; border-right: 1px solid #000000;")  # Updated

            layout = QVBoxLayout()
            self.setLayout(layout)

            pixmap = QPixmap(self.logo_path)
            logo_label = QLabel()
            logo_label.setPixmap(pixmap.scaled(QSize(50, 50), Qt.AspectRatioMode.KeepAspectRatio))
            logo_label.setStyleSheet("background-color: transparent;")
            layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

            self.buttons = {}
            for name, icon_path in self.icons.items():
                btn = QPushButton()
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(24, 24))
                btn.setToolTip(name.capitalize())
                btn.setStyleSheet("border: none; background-color: #E4E4E2;")  # Updated
                btn.clicked.connect(lambda checked, name=name: self.buttonClicked.emit(name))
                self.buttons[name] = btn
                layout.addWidget(btn)

            layout.addStretch()

            # Removed the indicator creation and addition code

            self.active_button = None
        except Exception as e:
            print(f"Error in SidePanel.initUI: {e}")

    def setActiveButton(self, name):
        try:
            if self.active_button:
                self.active_button.setStyleSheet("border: none; background-color: #E4E4E2;")  # Updated
            btn = self.buttons[name]
            btn.setStyleSheet("border: none; background-color: #82D19C;")  # Updated
            self.active_button = btn
        except Exception as e:
            print(f"Error in SidePanel.setActiveButton: {e}")


    def moveIndicator(self, btn):
        try:
            animation = QPropertyAnimation(self.indicator, b"geometry")
            animation.setDuration(300)
            animation.setStartValue(self.indicator.geometry())
            animation.setEndValue(QRect(btn.geometry().left() - 10, btn.geometry().top(), 10, 40))
            animation.start()
        except Exception as e:
            print(f"Error in SidePanel.moveIndicator: {e}")

    def enterEvent(self, event):
        try:
            self.setFixedWidth(200)
            for name, btn in self.buttons.items():
                btn.setText(btn.toolTip())
        except Exception as e:
            print(f"Error in SidePanel.enterEvent: {e}")

    def leaveEvent(self, event):
        try:
            self.setFixedWidth(60)
            for btn in self.buttons.values():
                btn.setText("")
        except Exception as e:
            print(f"Error in SidePanel.leaveEvent: {e}")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        window.resize(1000, 800)
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error in __main__: {e}")