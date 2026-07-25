import functools
import inspect
from pathlib import Path

from ...utils.css import Css


def window(css=None):
    """
    Декоратор для классов окон (QMainWindow/QDialog).
    После __init__ подгружает .css: либо явно указанный путь (css=...),
    либо зеркальный — файл модуля .../frontend/<путь>.py сопоставляется
    с .../styles/css/<путь>.css. Если файла нет — просто пропускается,
    без падения приложения.
    """
    def decorator(cls):
        original_init = cls.__init__

        @functools.wraps(original_init)
        def wrapped_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            css_path = css or _resolve_css_path(cls)
            if css_path and Path(css_path).is_file():
                Css.load(css_path, self)

        cls.__init__ = wrapped_init
        return cls

    return decorator


def _resolve_css_path(cls):
    module_file = Path(inspect.getfile(cls)).resolve()
    parts = module_file.parts

    if 'frontend' not in parts:
        return None

    idx = parts.index('frontend')
    mirrored = Path(*parts[:idx], 'styles', 'css', *parts[idx + 1:])
    return str(mirrored.with_suffix('.css'))
