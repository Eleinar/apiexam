from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QHBoxLayout)

class CatDialog(QDialog): # Диалоговое окно с информацией
    def __init__(self, cat):
        super().__init__()
        self.setWindowTitle(f"Информация о коте: {cat.get('name', '')}")
        self.cat = cat.copy()

        self.layout = QVBoxLayout()

        self.name_edit = QLineEdit(self.cat.get("name", "")) # Получение названия
        self.origin_edit = QLineEdit(self.cat.get("origin", "")) # Получение происхождения
        self.temperament_edit = QTextEdit(self.cat.get("temperament", "")) # Получение темперамента
        # Запрет на редактирования (до нажатия кнопки)
        self.name_edit.setReadOnly(True)
        self.origin_edit.setReadOnly(True)
        self.temperament_edit.setReadOnly(True)

        self.edit_button = QPushButton("Редактировать")
        self.edit_button.clicked.connect(self.toggle_edit)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_changes)
        self.save_button.setEnabled(False)

        self.layout.addWidget(QLabel("Имя:"))
        self.layout.addWidget(self.name_edit)
        self.layout.addWidget(QLabel("Происхождение:"))
        self.layout.addWidget(self.origin_edit)
        self.layout.addWidget(QLabel("Темперамент:"))
        self.layout.addWidget(self.temperament_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.save_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def toggle_edit(self): # Разрешение редактирования
        editable = not self.name_edit.isReadOnly() # Флаг редактируем/не редактируем
        # Смена доступа
        self.name_edit.setReadOnly(editable) 
        self.origin_edit.setReadOnly(editable)
        self.temperament_edit.setReadOnly(editable)
        self.save_button.setEnabled(not editable)

    def save_changes(self): # Сохранение изменений
        self.cat["name"] = self.name_edit.text()
        self.cat["origin"] = self.origin_edit.text()
        self.cat["temperament"] = self.temperament_edit.toPlainText()
        self.accept()
