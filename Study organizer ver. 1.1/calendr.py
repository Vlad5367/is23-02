import sys
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
                             QStackedWidget, QLineEdit, QTextEdit, QListWidget, QListWidgetItem, QFileDialog, QDialog,
                             QDialogButtonBox, QComboBox, QCalendarWidget)
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QRect, QPoint, pyqtSignal, QDateTime
from PyQt6.QtGui import QFont, QIcon, QPixmap

class CalendarWidget(QWidget):
    def init(self):
        super().init()
        self.notes = {}
        self.load_notes()
        self.initUI()

    def initUI(self):
        Calendarlayout = QVBoxLayout()

        # Добавление кнопок переключения вида
        self.view_selector = QComboBox()
        self.view_selector.addItems(["Месяц", "Неделя"])
        self.view_selector.currentIndexChanged.connect(self.change_view)
        Calendarlayout.addWidget(self.view_selector)

        self.calendar = QCalendarWidget()
        self.calendar.clicked.connect(self.show_note)
        Calendarlayout.addWidget(self.calendar)

        self.note_area = QTextEdit()
        Calendarlayout.addWidget(self.note_area)

        self.save_button = QPushButton("Сохранить заметку")
        self.save_button.clicked.connect(self.save_note)
        Calendarlayout.addWidget(self.save_button)

        self.setLayout(Calendarlayout)

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
            self.delete_button.setStyleSheet("background-color: #FF6961; border-radius: 10px; padding: 10px;")
            self.delete_button.clicked.connect(self.delete_note)
            self.note_detail_layout.addWidget(self.delete_button)

            self.favorite_button = QPushButton("☆")
            self.favorite_button.setFont(QFont("Arial", 12))
            self.favorite_button.setStyleSheet("background-color: #FFD700; border-radius: 10px; padding: 10px;")
            self.favorite_button.clicked.connect(self.toggle_favorite)
            self.note_detail_layout.addWidget(self.favorite_button)

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
            self.load_notes()
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
        window.resize(1000, 800)
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error in __main__: {e}")
