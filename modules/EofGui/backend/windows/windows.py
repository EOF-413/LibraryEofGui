import functools

from PyQt5.QtCore import QObject, pyqtSignal

# Local
from ....LogSystem import log_init

log = log_init('EofGui/backend')


class Controller(QObject):
    """
    Базовый класс для backend-логики окна. Даёт общий сигнал ошибок
    (error_occurred) и декоратор Controller.guarded, который перехватывает
    исключение в методе, пишет его в лог и эмитит error_occurred вместо
    ручного try/except в каждом обработчике.
    """
    error_occurred = pyqtSignal(str, str)

    @staticmethod
    def guarded(title):
        def decorator(func):
            @functools.wraps(func)
            def wrapped(self, *args, **kwargs):
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    log.error(f"Ошибка в [{func.__qualname__}]: {e}")
                    self.error_occurred.emit(title, str(e))
                    return None
            return wrapped
        return decorator
