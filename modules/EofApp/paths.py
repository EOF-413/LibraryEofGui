import sys

from os import (
    path
)


class AppType:
    @staticmethod
    def is_exe():
        return getattr(sys, 'frozen', False)

    @staticmethod
    def is_source():
        return not getattr(sys, 'frozen', False)


class AppPaths:
    @staticmethod
    def root():
        if AppType.is_exe():
            return path.dirname(sys.executable)
        else:
            return path.abspath(path.join(path.dirname(__file__), '..', '..'))

    @staticmethod
    def resource(relative_path):
        relative_path = relative_path.split('/') if isinstance(relative_path, str) else list(relative_path)

        if AppType.is_exe():
            return path.join(sys._MEIPASS, *relative_path)
        else:
            return path.join(AppPaths.root(), *relative_path)

    @staticmethod
    def logs():
        return path.join(AppPaths.root(), 'logs')

    @staticmethod
    def temp():
        if AppType.is_exe():
            return path.join(path.dirname(sys.executable), 'temp')
        else:
            return path.join(AppPaths.root(), 'temp')
