from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QMessageBox)
import requests
from cat_dialog import CatDialog

def load_cats():
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

class MainWindow(QMainWindow):
    cat_updated = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Котики")
        self.setGeometry(100, 100, 800, 600)

        self.cats = load_cats()
        self.filtered_cats = self.cats.copy()

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Имя", "Происхождение", "Темперамент"])
        self.table.doubleClicked.connect(self.open_cat_dialog)

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Все")
        self.origins = sorted({cat.get("origin", "") for cat in self.cats})
        self.filter_combo.addItems(self.origins)
        self.filter_combo.currentIndexChanged.connect(self.apply_filter)

        self.delete_button = QPushButton("Удалить выбранного кота")
        self.delete_button.clicked.connect(self.delete_selected_cat)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Фильтр по происхождению:"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.delete_button)

        self.layout_v = QVBoxLayout()
        self.layout_v.addLayout(filter_layout)
        self.layout_v.addWidget(self.table)

        widget = QWidget()
        widget.setLayout(self.layout_v)
        self.setCentralWidget(widget)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(len(self.filtered_cats))
        for row, cat in enumerate(self.filtered_cats):
            self.table.setItem(row, 0, QTableWidgetItem(cat.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(cat.get("origin", "")))
            self.table.setItem(row, 2, QTableWidgetItem(cat.get("temperament", "")))

    def apply_filter(self):
        selected_origin = self.filter_combo.currentText()
        if selected_origin == "Все":
            self.filtered_cats = self.cats.copy()
        else:
            self.filtered_cats = [cat for cat in self.cats if cat.get("origin") == selected_origin]
        self.update_table()

    def open_cat_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            return
        cat = self.filtered_cats[row]
        dialog = CatDialog(cat, self)
        if dialog.exec():
            self.cats = [dialog.cat if c['id'] == cat['id'] else c for c in self.cats]
            self.apply_filter()

    def delete_selected_cat(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите кота для удаления.")
            return

        reply = QMessageBox.question(self, "Удалить?", "Точно удалить этого кота?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            cat = self.filtered_cats[row]
            self.cats = [c for c in self.cats if c['id'] != cat['id']]
            self.apply_filter()
