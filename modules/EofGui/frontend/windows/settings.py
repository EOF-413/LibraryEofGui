from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QLineEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QPushButton
)


class AutoFormDialog(QDialog):
    """
    Диалог, который сам строит форму полей по словарю {ключ: значение}
    (тип поля определяется типом значения). Наследник задаёт заголовок и
    исходные данные через конструктор, а сохранение — переопределив on_save.
    """

    def __init__(self, title, data, empty_hint=None, parent=None):
        super().__init__(parent)
        self._fields = {}
        self.data = data

        self.setWindowTitle(title)

        root = QVBoxLayout(self)

        if not data:
            hint = QLabel(empty_hint or 'Настроек пока нет.')
            hint.setObjectName('SettingsHint')
            root.addWidget(hint)
        else:
            form = QFormLayout()
            for key, value in data.items():
                field = self._build_field(value)
                self._fields[key] = field
                form.addRow(key, field)
            root.addLayout(form)

        buttons = QHBoxLayout()
        buttons.addStretch(1)
        cancel_btn = QPushButton('Отмена')
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton('Сохранить')
        save_btn.clicked.connect(self._on_save)
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        root.addLayout(buttons)

    def _build_field(self, value):
        if isinstance(value, bool):
            field = QCheckBox()
            field.setChecked(value)
        elif isinstance(value, int):
            field = QSpinBox()
            field.setRange(-1000000000, 1000000000)
            field.setValue(value)
        elif isinstance(value, float):
            field = QDoubleSpinBox()
            field.setRange(-1000000000, 1000000000)
            field.setValue(value)
        else:
            field = QLineEdit(str(value))
        return field

    def _collect(self):
        updated = dict(self.data) if self.data else {}
        for key, field in self._fields.items():
            if isinstance(field, QCheckBox):
                updated[key] = field.isChecked()
            elif isinstance(field, (QSpinBox, QDoubleSpinBox)):
                updated[key] = field.value()
            else:
                updated[key] = field.text()
        return updated

    def _on_save(self):
        self.on_save(self._collect())
        self.accept()

    def on_save(self, data):
        raise NotImplementedError
