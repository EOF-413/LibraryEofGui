import sys

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton
)

from modules import (
    AppPaths,
    AutoFormDialog,
    Css,
    window,
    log_init,
)

log = log_init('main')


class SettingsDialog(AutoFormDialog):
    def __init__(self, parent=None):
        data = {
            "Имя пользователя": "Admin",
            "Email": "admin@example.com",
            "Автозапуск": True,
            "Порт": 8080,
            "Таймаут": 30.5
        }
        super().__init__(
            title="Настройки приложения",
            data=data,
            empty_hint="Нет настроек для отображения",
            parent=parent
        )

    def on_save(self, data):
        log.info(f"Настройки сохранены: {data}")
        print(f"Сохранено: {data}")


@window()
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Тестовое окно LEG")
        self.setGeometry(100, 100, 400, 300)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        label = QLabel("Привет из LibraryEofGui (LEG)!")
        label.setObjectName("TitleLabel")
        layout.addWidget(label)

        desc = QLabel("Нажмите кнопку для открытия настроек")
        desc.setObjectName("DescLabel")
        layout.addWidget(desc)

        btn_settings = QPushButton("Открыть настройки")
        btn_settings.setObjectName("SettingsBtn")
        btn_settings.clicked.connect(self.open_settings)
        layout.addWidget(btn_settings)

        btn_log = QPushButton("Тестовый лог")
        btn_log.setObjectName("LogBtn")
        btn_log.clicked.connect(self.test_log)
        layout.addWidget(btn_log)

        btn_close = QPushButton("Закрыть")
        btn_close.setObjectName("CloseBtn")
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        log.info("Главное окно создано")

    def open_settings(self):
        log.info("Открытие настроек")
        dialog = SettingsDialog(self)
        dialog.exec_()

    def test_log(self):
        log.debug("Тестовый DEBUG")
        log.info("Тестовый INFO")
        log.warning("Тестовый WARNING")
        log.error("Тестовый ERROR")
        log.critical("Тестовый CRITICAL")
        print("Логи записаны в logs/main/")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("LEG Test")

    log.info("Приложение запущено")
    print(f"AppPaths.root(): {AppPaths.root()}")
    print(f"AppPaths.logs(): {AppPaths.logs()}")

    Css.load(AppPaths.resource('styles/main.css'))

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
