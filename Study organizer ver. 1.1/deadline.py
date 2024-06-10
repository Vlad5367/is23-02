import sys
import json
from datetime import datetime
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QFrame, \
    QScrollArea, QGridLayout, QMenu, QDialog, QLineEdit, QDateTimeEdit, QFormLayout, QDialogButtonBox, QComboBox, QMessageBox
from PyQt6.QtCore import Qt, QTimer


class TaskCard(QWidget):
    def __init__(self, title, deadline, task_name, subject):
        super().__init__()
        self.initUI(title, deadline, task_name, subject)

    def initUI(self, title, deadline, task_name, subject):
        layout = QVBoxLayout()

        self.titleLabel = QLabel(title)
        self.deadlineLabel = QLabel(deadline)
        self.taskNameLabel = QPushButton(task_name)
        self.taskNameLabel.setStyleSheet("background-color: #E4E4E2; border: none;")
        self.subjectLabel = QPushButton(subject)
        self.subjectLabel.setStyleSheet("background-color: #E4E4E2; border: none;")

        menuButton = QPushButton("...")
        menuButton.setFixedSize(30, 30)
        menuButton.clicked.connect(self.showMenu)

        layout.addWidget(self.titleLabel)
        layout.addWidget(self.deadlineLabel)
        layout.addWidget(self.taskNameLabel)
        layout.addWidget(self.subjectLabel)
        layout.addWidget(menuButton)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #F9F9F9; border-radius: 10px; padding: 10px;")

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
        dialog.deadlineEdit.setDateTime(datetime.strptime(self.deadlineLabel.text(), '%d.%m.%Y %H:%M'))
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
                    window.tasksLayout.addWidget(self)
                else:
                    window.inProgressLayout.addWidget(self)

            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, MainWindow):
                    widget.saveTasks()
                    break

    def deleteTask(self):
        self.setParent(None)
        window.saveTasks()

    def archiveTask(self):
        window.archiveWindow.addArchivedTask(self)
        window.saveTasks()


class AddTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить задание')
        self.setGeometry(100, 100, 300, 300)

        layout = QFormLayout()

        self.titleEdit = QLineEdit()
        self.deadlineEdit = QDateTimeEdit(calendarPopup=True)
        self.deadlineEdit.setDateTime(datetime.now())
        self.taskNameEdit = QLineEdit()
        self.subjectEdit = QLineEdit()
        self.categoryComboBox = QComboBox()
        self.categoryComboBox.addItems(["Задачи", "В процессе"])

        layout.addRow('Название:', self.titleEdit)
        layout.addRow('Дедлайн:', self.deadlineEdit)
        layout.addRow('Название работы:', self.taskNameEdit)
        layout.addRow('Предмет:', self.subjectEdit)
        layout.addRow('Категория:', self.categoryComboBox)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def validate(self):
        if not self.titleEdit.text() or not self.deadlineEdit.text() or not self.taskNameEdit.text() or not self.subjectEdit.text():
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены")
        else:
            self.accept()

    def getTaskData(self):
        return (
            self.titleEdit.text(),
            self.deadlineEdit.dateTime().toString('dd.MM.yyyy HH:mm'),
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

        mainWidget = QWidget()
        mainLayout = QVBoxLayout()

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

        mainLayout.addLayout(tasksColumn)

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    def addArchivedTask(self, task):
        self.tasksLayout.addWidget(task)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.archiveWindow = ArchiveWindow()
        self.loadTasks()
        self.initTimer()

    def initUI(self):
        self.setWindowTitle('Задачи и дедлайны')
        self.setGeometry(100, 100, 800, 600)

        mainWidget = QWidget()
        mainLayout = QVBoxLayout()

        headerLayout = QHBoxLayout()

        titleLabel = QLabel("Задачи и дедлайны")
        descriptionLabel = QLabel("Сделай каждый дедлайн достижимым. Управляй задачами с умом в Study Organizer.")

        headerRightLayout = QVBoxLayout()
        addButton = QPushButton("Добавить")
        addButton.setStyleSheet("background-color: #82D19C; border-radius: 10px;")
        addButton.clicked.connect(self.showAddTaskDialog)
        archiveButton = QPushButton("Архив")
        archiveButton.setStyleSheet("background-color: #E4E4E2; border: none; color: blue; text-decoration: underline;")
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

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

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

        data = {
            "tasks": tasks,
            "in_progress": in_progress,
            "archived": archived
        }

        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def loadTasks(self):
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
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
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkDeadlines)
        self.timer.start(60)

    def checkDeadlines(self):
        current_time = datetime.now()
        tasks_to_archive = []

        for i in range(self.tasksLayout.count()):
            task = self.tasksLayout.itemAt(i).widget()
            if task:
                try:
                    deadline = datetime.strptime(task.deadlineLabel.text(), '%d.%m.%Y %H:%M')
                    if current_time >= deadline:
                        tasks_to_archive.append(task)
                except ValueError:
                    pass  # Handle invalid date format

        for task in tasks_to_archive:
            task.setParent(None)
            self.archiveTask(task)

        tasks_to_archive.clear()

        for i in range(self.inProgressLayout.count()):
            task = self.inProgressLayout.itemAt(i).widget()
            if task:
                try:
                    deadline = datetime.strptime(task.deadlineLabel.text(), '%d.%m.%Y %H:%M')
                    if current_time >= deadline:
                        tasks_to_archive.append(task)
                except ValueError:
                    pass  # Handle invalid date format

        for task in tasks_to_archive:
            task.setParent(None)
            self.archiveTask(task)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())