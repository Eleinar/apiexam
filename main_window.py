from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox, QPushButton)
import requests

def load_cats():
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Котики")
        self.setGeometry(100,100,800,600)
        
        self.cats = load_cats()
        self.filter_cats = self.cats.copy()
        
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Имя", "Происхождение", "Темперамент"])
        self.table.doubleClicked.connect(self.open_cat_info)
        
        self.filter = QComboBox()
        self.filter.addItem("Все")
        self.origins = self.cats.get("origin", "")
        self.filter.addItems(self.origins)
        self.filter.currentIndexChanged.connect(self.apply_filter)
        
        self.delete_button = QPushButton("Удалить кота")
        self.delete_button.clicked.connect(self.delete_cat)
        
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(QLabel("Происхождение:"))
        filter_layout.addWidget(self.filter)
        filter_layout.addWidget(self.delete_button)
        
        layout_h = QHBoxLayout()
        layout_h.addLayout(self.filter)
        layout_h.addWidget(self.table)
        
        widget = QWidget()
        widget.setLayout(self.layout_h)
        self.setCentralWidget(widget)
        
        self.update_table()
    
    def update_table(self):
        self.table.setRowCount(len(self.filter_cats))
        for row, cat in enumerate(self.filter_cats):
            self.table.setItem(row, 0, QTableWidgetItem(cat.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(cat.get("origin", "")))
            self.table.setItem(row, 2, QTableWidgetItem(cat.get("temperament", "")))
            
    def apply_filter(self):
        selected_origin = self.filter.currentText()
        if selected_origin == "Все":
            self.filter_cats = self.cats.copy()
        else:
            self.filter_cats = [cat for cat in self.cats if cat.get("origin" == selected_origin)]
        self.update_table