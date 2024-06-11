import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
                             QStackedWidget, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QFileDialog, QDialog,
                             QDialogButtonBox, QCalendarWidget)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap

class Note:
    def __init__(self, title, subtitle, description, image_path=None, favorite=False):
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.image_path = image_path
        self.favorite = favorite

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

            self.note_title = QLabel()
            self.note_title.setFont(QFont("Arial", 16))
            self.note_detail_layout.addWidget(self.note_title)

            self.note_subtitle = QLabel()
            self.note_subtitle.setFont(QFont("Arial", 14))
            self.note_detail_layout.addWidget(self.note_subtitle)

            self.note_description = QTextEdit()
            self.note_description.setReadOnly(True)
            self.note_detail_layout.addWidget(self.note_description)

            self.edit_button = QPushButton("Редактировать")
            self.edit_button.setFont(QFont("Arial", 12))
            self.edit_button.setStyleSheet("background-color: #FFA07A; border-radius: 10px; padding: 10px;")
            self.edit_button.clicked.connect(self.edit_note)
            self.note_detail_layout.addWidget(self.edit_button)

            main_layout.addWidget(self.note_detail_widget)

            self.add_button = QPushButton("✍ Добавить")
            self.add_button.setFont(QFont("Arial", 12))
            self.add_button.setStyleSheet("background-color: #A8E6CF; border-radius: 10px; padding: 10px;")
            self.add_button.clicked.connect(self.add_note)
            main_layout.addWidget(self.add_button)

            self.setLayout(main_layout)
        except Exception as e:
            print(f"Error in NotesWidget.initUI: {e}")

    def display_note(self, item):
        try:
            note = self.notes[self.notes_list.row(item)]
            self.note_title.setText(note.title)
            self.note_subtitle.setText(note.subtitle)
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
                self.note_title.setText(f"Edit: {note.title}")
                self.edit_note_dialog(note)
        except Exception as e:
            print(f"Ошибка: {e}")

    def add_note_to_list(self, note, index=None):
        try:
            item = QListWidgetItem(f"{note.title}\n{note.subtitle}")
            if note.favorite:
                item.setBackground(Qt.GlobalColor.yellow)
            if index is not None:
                self.notes_list.insertItem(index, item)
            else:
                self.notes_list.addItem(item)
        except Exception as e:
            print(f"Error in NotesWidget.add_note_to_list: {e}")

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
        except Exception as e:
            print(f"Error in NotesWidget.edit_note_dialog: {e}")

class NoteEditDialog(QDialog):
    def __init__(self, note, parent=None):
        super().__init__(parent)
        self.note = note
        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle('Редактировать')
            layout = QVBoxLayout(self)

            self.title_edit = QLineEdit(self.note.title)
            self.subtitle_edit = QLineEdit(self.note.subtitle)
            self.description_edit = QTextEdit(self.note.description)

            layout.addWidget(QLabel('Заголовок:'))
            layout.addWidget(self.title_edit)
            layout.addWidget(QLabel('Подзаголовок:'))
            layout.addWidget(self.subtitle_edit)
            layout.addWidget(QLabel('Описание:'))
            layout.addWidget(self.description_edit)

            self.image_label = QLabel()
            self.image_label.setFixedSize(200, 200)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if self.note.image_path:
                pixmap = QPixmap(self.note.image_path)
                self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(self.image_label)

            self.upload_button = QPushButton("Загрузить изображение")
            self.upload_button.clicked.connect(self.upload_image)
            layout.addWidget(self.upload_button)

            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)
        except Exception as e:
            print(f"Error in NoteEditDialog.initUI: {e}")

    def upload_image(self):
        try:
            file_dialog = QFileDialog(self, "Выбрать изображение", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                if file_path:
                    self.note.image_path = file_path
                    pixmap = QPixmap(file_path)
                    self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            print(f"Error in NoteEditDialog.upload_image: {e}")

    def accept(self):
        try:
            self.note.title = self.title_edit.text()
            self.note.subtitle = self.subtitle_edit.text()
            self.note.description = self.description_edit.toPlainText()
            super().accept()
        except Exception as e:
            print(f"Error in NoteEditDialog.accept: {e}")

class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.show_notes_for_selected_date)
        layout.addWidget(self.calendar)

        self.notes_text = QTextEdit()
        layout.addWidget(self.notes_text)

        self.save_button = QPushButton("Сохранить заметку")
        self.save_button.clicked.connect(self.save_note_for_selected_date)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def show_notes_for_selected_date(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        note = self.notes.get(selected_date, "")
        self.notes_text.setText(note)

    def save_note_for_selected_date(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        note = self.notes_text.toPlainText()
        self.notes[selected_date] = note
        print(f"Заметка сохранена для {selected_date}: {note}")

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
                'Календарь': 'icon_calendar.png'
            }
            self.side_panel = SidePanel(logo_path, icons)
            self.side_panel.buttonClicked.connect(self.changePage)
            content_layout.addWidget(self.side_panel)

            self.stack = QStackedWidget()
            self.pages = {
                'Главная': QWidget(),
                '   Цели': QWidget(),
                'Конспекты': NotesWidget(),
                'Календарь': CalendarWidget()
            }
            for page in self.pages.values():
                self.stack.addWidget(page)

            content_layout.addWidget(self.stack)
            self.changePage('Главная')
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
            self.setStyleSheet("background-color: #E0E0E0;")

            layout = QVBoxLayout()
            self.setLayout(layout)

            pixmap = QPixmap(self.logo_path)
            logo_label = QLabel()
            logo_label.setPixmap(pixmap.scaled(QSize(40, 40), Qt.AspectRatioMode.KeepAspectRatio))
            layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

            self.buttons = {}
            for name, icon_path in self.icons.items():
                btn = QPushButton()
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(QSize(24, 24))
                btn.setToolTip(name.capitalize())
                btn.setStyleSheet("border: none;")
                btn.clicked.connect(lambda checked, name=name: self.buttonClicked.emit(name))
                self.buttons[name] = btn
                layout.addWidget(btn)

            layout.addStretch()

            self.indicator = QLabel()
            self.indicator.setStyleSheet("background-color: #82D19C;")
            self.indicator.setFixedWidth(10)
            self.indicator.setFixedHeight(40)
            self.indicator.move(50, 0)
            self.indicator.setParent(self)
            self.active_button = None
        except Exception as e:
            print(f"Error in SidePanel.initUI: {e}")

    def setActiveButton(self, name):
        try:
            if self.active_button:
                self.active_button.setStyleSheet("border: none;")
            btn = self.buttons[name]
            btn.setStyleSheet("border: none; background-color: #82D19C;")
            self.active_button = btn
            self.moveIndicator(btn)
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
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error in __main__: {e}")
