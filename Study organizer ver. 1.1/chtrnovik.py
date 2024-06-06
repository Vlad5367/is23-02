import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap

class ImageLoaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Загрузчик изображений")
        self.setGeometry(100, 100, 800, 600)

        # Создаем центральный виджет и устанавливаем его как центральный виджет главного окна
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем вертикальный макет
        layout = QVBoxLayout(central_widget)

        # Создаем кнопку для загрузки изображения
        self.button = QPushButton("Загрузить изображение", self)
        self.button.clicked.connect(self.load_image)
        layout.addWidget(self.button)

        # Создаем метку для отображения изображения
        self.label = QLabel(self)
        layout.addWidget(self.label)

    def load_image(self):
        try:
            # Открываем диалоговое окно для выбора файла изображения
            file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать изображение", "", "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file_name:
                # Загружаем и отображаем изображение в метке
                pixmap = QPixmap(file_name)
                self.label.setPixmap(pixmap)
                self.label.setScaledContents(True)  # Изображение масштабируется по размеру метки
        except Exception as e:
            print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        main_window = ImageLoaderApp()
        main_window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Произошла ошибка при запуске приложения: {e}")
