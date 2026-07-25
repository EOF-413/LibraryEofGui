# LibraryEofGui (LEG)

**LEG** - это библиотека для работы с PyQt5 интерфейсом. Содержит утилиты для загрузки CSS, построения форм, layout'ов и работы с путями.

## Особенности

- Загрузка и применение CSS стилей
- Автоматическое построение диалогов настроек
- Кастомный FlowLayout
- Декораторы для автоматической загрузки стилей окон
- Работа с путями (поддержка .exe и source режимов)
- Интеграция с LibraryLogSystem (LLS)

## Установка

```py
from modules import (
    AppPaths,
    AutoFormDialog,
    Css,
    window,
    log_init,
)
```

## Использование

### CSS Utils (utils/css.py)

Загрузка и применение CSS стилей.

```py
from modules import AppPaths, AppType, Css

# Загрузка глобальных стилей
Css.load(AppPaths.resource('styles/main.css'))

# Загрузка стилей для конкретного виджета
Css.load('styles/widget.css', widget)
```

### Paths Utils (EofApp/paths.py)

Работа с путями в приложении.

```py
from modules import AppPaths, AppType

# Проверка типа приложения
if AppType.is_exe():
    print("Запущено как .exe")
else:
    print("Запущено из исходного кода")

# Получение путей
root = AppPaths.root()              # Корневая директория
logs = AppPaths.logs()              # Директория логов
temp = AppPaths.temp()              # Временная директория
resource = AppPaths.resource('styles/main.css')  # Путь к ресурсу
```

### Flow Layout (frontend/flow.py)

Кастомный FlowLayout для автоматического переноса элементов.

```py
from modules import FlowLayout

layout = FlowLayout()
layout.addWidget(widget1)
layout.addWidget(widget2)
layout.addWidget(widget3)
```

### Windows Decorator (frontend/windows.py)

Декоратор для автоматической загрузки CSS стилей для окон.

```py
from modules import window

# С указанием пути к CSS
@window(css='styles/my_window.css')
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

# Автоматическое определение пути
@window()
class AnotherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Стиль загрузится из styles/css/путь_к_файлу.css
```

### Settings Dialog (frontend/settings.py)

Диалог настроек с автоматическим построением формы.

```py
from modules import AutoFormDialog

class MySettings(AutoFormDialog):
    def __init__(self, parent=None):
        data = {
            "Имя пользователя": "Admin",
            "Email": "admin@example.com",
            "Порт": 8080,
            "Автозапуск": True,
            "Таймаут": 30.5
        }
        super().__init__(
            title="Настройки приложения",
            data=data,
            empty_hint="Нет настроек для отображения",
            parent=parent
        )
    
    def on_save(self, data):
        print(f"Сохранено: {data}")
```

### Controller (backend/windows.py)

Базовый контроллер с обработкой ошибок.

```py
from modulesimport Controller

class MyController(Controller):
    @Controller.guarded("Ошибка загрузки")
    def load_data(self):
        raise ValueError("Ошибка")
```

## API

### Css.load()

```py
Css.load(file_path, widget=None)
```

Загружает CSS файл и применяет к виджету или приложению.

Параметры:

```py
- file_path (str): Путь к CSS файлу
- widget (QWidget, optional): Виджет для применения стилей
```

Возвращает:

```py
- str: Содержимое CSS файла или None при ошибке
```

### AppPaths.root()

```py
AppPaths.root()
```

Возвращает корневую директорию приложения.

### AppPaths.resource()

```py
AppPaths.resource(relative_path)
```

Возвращает путь к ресурсу (поддерживает .exe и source).

### AppPaths.logs()

```py
AppPaths.logs()
```

Возвращает директорию для логов.

### AppPaths.temp()

```py
AppPaths.temp()
```

Возвращает временную директорию.

### AppType.is_exe()

```py
AppType.is_exe()
```

Проверяет, запущено ли приложение как .exe.

### AppType.is_source()

```py
AppType.is_source()
```

Проверяет, запущено ли приложение из исходного кода.

### @window(c)

```py
@window(css=None)
```

Декоратор для автоматической загрузки CSS стилей в окно.

### AutoFormDialog

Диалог с автоматическим построением формы по словарю данных.

### FlowLayout

Кастомный FlowLayout для PyQt5.

## Структура

```text
modules/EofGui/
├── utils/
│   ├── css.py           # Загрузка CSS
│   └── paths.py         # Работа с путями
├── frontend/
│   ├── windows.py       # Декораторы окон
│   ├── settings.py      # Диалог настроек
│   └── flow.py          # FlowLayout
└── backend/
    └── windows.py       # Контроллеры окон
```

## Зависимости
[PyQt5](https://pypi.org/project/PyQt5/)
[LibraryEofApp (LEA)](https://github.com/EOF-413/LibraryEofApp)
[LibraryLogSystem (LLS)](https://github.com/EOF-413/LibraryLogSystem)
