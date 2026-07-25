# Download
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream

# Local
from ...LogSystem import log_init

log = log_init('EofGui/utils')


class Css:
    @staticmethod
    def load(file_path, widget=None):
        file = QFile(file_path)
        if not file.open(QFile.ReadOnly | QFile.Text):
            log.error(f"Не удалось открыть файл стилей: {file_path}")
            return None

        stream = QTextStream(file)
        style = stream.readAll()
        file.close()

        if widget is not None:
            widget.setStyleSheet(style)
        else:
            app = QApplication.instance()
            if app is not None:
                app.setStyleSheet(style)
            else:
                log.error("Нет экземпляра QApplication.")
                return style
        return style
