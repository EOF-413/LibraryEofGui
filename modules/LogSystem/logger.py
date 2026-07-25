from os import (
    path,
    getcwd,
    remove,
    listdir,
    makedirs,
)

from datetime import datetime

from logging import (
    getLogger,
    DEBUG,
    INFO,
    WARNING,
    ERROR,
    CRITICAL,
    Filter,
    Formatter,
    NullHandler,
    LogRecord
)

from logging.handlers import RotatingFileHandler


class LevelFilter(Filter):
    def __init__(self, levels):
        self.levels = levels
        super().__init__()

    def filter(self, record):
        return record.levelno in self.levels


class CriticalFilter(Filter):
    def filter(self, record):
        return record.levelno >= CRITICAL


class LoggerSystem:
    _instances = {}
    _global_start_time = datetime.now()

    def __new__(cls, folder="default"):
        if folder not in cls._instances:
            instance = super().__new__(cls)
            instance._initialized = False
            cls._instances[folder] = instance
        return cls._instances[folder]

    def __init__(self, folder="default"):
        if self._initialized:
            return

        self.folder = folder
        self.logger = None
        self.start_time = LoggerSystem._global_start_time
        self._initialized = False

    def _clear(self, log_dir, keep=5):
        if not path.exists(log_dir):
            return

        log_files = [f for f in listdir(log_dir) if f.endswith('.log')]

        if len(log_files) <= keep:
            return

        log_files.sort()

        for old_file in log_files[:-keep]:
            try:
                remove(path.join(log_dir, old_file))
            except Exception:
                pass

    def _write_init(self, log_file):
        formatter = Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s] '
            '[%(funcName)s] [%(lineno)d] -> %(message)s',
            datefmt='%d.%m.%Y %H:%M:%S'
        )

        record = LogRecord(
            name='logger.py',
            level=INFO,
            pathname='logger.py',
            lineno=0,
            msg=f"Логирование инициализировано для [{self.folder}]: {self.start_time.strftime('%H:%M:%S %d.%m.%Y')}.",
            args=(),
            exc_info=None,
            func='<module>'
        )
        record.asctime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(formatter.format(record) + '\n')

    def _path(self, category):
        logs_dir = path.join(getcwd(), "logs", self.folder)
        category_dir = path.join(logs_dir, category)
        makedirs(category_dir, exist_ok=True)

        time_str = self.start_time.strftime("%H.%M.%S_%d.%m.%Y")
        log_file = path.join(category_dir, f"{time_str}.log")

        if not path.exists(log_file):
            self._write_init(log_file)

        self._clear(category_dir, 5)
        return log_file

    def _all_path(self):
        all_dir = path.join(getcwd(), "logs", "all")
        makedirs(all_dir, exist_ok=True)

        time_str = self.start_time.strftime("%H.%M.%S_%d.%m.%Y")
        log_file = path.join(all_dir, f"{time_str}.log")

        return log_file

    def _write_all(self, log_file):
        if path.exists(log_file):
            return

        formatter = Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s] '
            '[%(funcName)s] [%(lineno)d] -> %(message)s',
            datefmt='%d.%m.%Y %H:%M:%S'
        )

        record = LogRecord(
            name='logger.py',
            level=INFO,
            pathname='logger.py',
            lineno=0,
            msg=f"Глобальное логирование инициализировано: {self.start_time.strftime('%H:%M:%S %d.%m.%Y')}.",
            args=(),
            exc_info=None,
            func='<module>'
        )
        record.asctime = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(formatter.format(record) + '\n')

    def setup(self):
        if self._initialized:
            return self.logger

        self.logger = getLogger(self.folder)
        self.logger.setLevel(DEBUG)
        self.logger.propagate = False

        categories = {
            "critical": CriticalFilter(),
            "errors": LevelFilter([ERROR]),
            "warnings": LevelFilter([WARNING]),
            "info": LevelFilter([INFO]),
            "debug": LevelFilter([DEBUG]),
        }

        formatter = Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s] '
            '[%(funcName)s] [%(lineno)d] -> %(message)s',
            datefmt='%d.%m.%Y %H:%M:%S'
        )

        for category_name, level_filter in categories.items():
            log_path = self._path(category_name)

            handler = RotatingFileHandler(
                log_path,
                maxBytes=10 * 1024 * 1024,
                backupCount=0,
                encoding='utf-8'
            )
            handler.setLevel(DEBUG)
            handler.addFilter(level_filter)
            handler.setFormatter(formatter)

            self.logger.addHandler(handler)

        all_log_path = self._all_path()
        self._write_all(all_log_path)

        all_handler = RotatingFileHandler(
            all_log_path,
            maxBytes=10 * 1024 * 1024,
            backupCount=0,
            encoding='utf-8'
        )
        all_handler.setLevel(DEBUG)
        all_handler.setFormatter(formatter)
        self.logger.addHandler(all_handler)

        self.logger.addHandler(NullHandler())
        self._initialized = True

        return self.logger

    def __getattr__(self, name):
        if not self._initialized:
            self.setup()

        short_names = {
            'd': 'debug',
            'i': 'info',
            'w': 'warning',
            'e': 'error',
            'c': 'critical'
        }

        if name in short_names:
            return getattr(self.logger, short_names[name])

        if name in ['debug', 'info', 'warning', 'error', 'critical']:
            return getattr(self.logger, name)

        raise AttributeError(f"'LoggerSystem' object has no attribute '{name}'")


_log_instances = {}


def log_init(folder="default"):
    if folder not in _log_instances:
        _log_instances[folder] = LoggerSystem(folder)
        _log_instances[folder].setup()
    return _log_instances[folder]
