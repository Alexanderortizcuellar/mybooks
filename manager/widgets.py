from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal
from .constants import TAG_FG, TEXT_DIM, TAG_BG, SURFACE2, BORDER, ACCENT
from .layouts import FlowLayout

class TagChip(QWidget):
    removed = pyqtSignal(str)

    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 4, 6, 4)
        layout.setSpacing(6)

        label = QLabel(text)
        label.setStyleSheet(
            f"color: {TAG_FG}; font-size: 12px; font-weight: 500; background: transparent; border: none;"
        )
        layout.addWidget(label)

        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(16, 16)
        remove_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                color: {TEXT_DIM};
                font-size: 14px;
                font-weight: bold;
                padding: 0;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                color: white;
                background: #ff4466;
            }}
        """)
        remove_btn.clicked.connect(lambda: self.removed.emit(self.text))
        layout.addWidget(remove_btn)

        self.setStyleSheet(f"""
            QWidget {{
                background: {TAG_BG};
                border: 1px solid #4c2885;
                border-radius: 12px;
            }}
        """)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

class TagInputWidget(QWidget):
    def __init__(self, placeholder="Add tag…", parent=None):
        super().__init__(parent)
        self.tags = []
        self._build_ui(placeholder)

    def _build_ui(self, placeholder):
        self.outer = QVBoxLayout(self)
        self.outer.setContentsMargins(0, 0, 0, 0)
        self.outer.setSpacing(6)

        # chips container (wrapping flow)
        self.chip_frame = QFrame()
        self.chip_frame.setStyleSheet(f"""
            QFrame {{
                background: {SURFACE2};
                border: 1px solid {BORDER};
                border-radius: 8px;
            }}
        """)
        self.chips_layout = FlowLayout(self.chip_frame)
        self.chips_layout.setContentsMargins(8, 8, 8, 8)
        self.chips_layout.setSpacing(6)
        self.chip_frame.setMinimumHeight(44)
        self.outer.addWidget(self.chip_frame)

        # input row
        row = QHBoxLayout()
        row.setSpacing(6)
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.returnPressed.connect(self._add_from_input)
        row.addWidget(self.input)

        add_btn = QPushButton("Add")
        add_btn.setFixedWidth(55)
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background: {TAG_BG};
                border: 1px solid #4c2885;
                border-radius: 8px;
                color: {ACCENT};
                font-size: 12px;
                font-weight: 600;
                padding: 7px 10px;
            }}
            QPushButton:hover {{
                background: #3d1f6e;
                border-color: {ACCENT};
            }}
        """)
        add_btn.clicked.connect(self._add_from_input)
        row.addWidget(add_btn)
        self.outer.addLayout(row)

    def _add_from_input(self):
        text = self.input.text().strip()
        if text:
            for part in text.split(","):
                self.add_tag(part.strip())
            self.input.clear()

    def add_tag(self, text):
        if text and text not in self.tags:
            self.tags.append(text)
            chip = TagChip(text)
            chip.removed.connect(self.remove_tag)
            self.chips_layout.addWidget(chip)
            self.chip_frame.setMinimumHeight(
                max(44, self.chips_layout.heightForWidth(self.chip_frame.width()) + 16)
            )

    def remove_tag(self, text):
        if text in self.tags:
            self.tags.remove(text)
        for i in range(self.chips_layout.count()):
            item = self.chips_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), TagChip):
                if item.widget().text == text:
                    w = self.chips_layout.takeAt(i).widget()
                    w.setParent(None)
                    w.deleteLater()
                    break

    def get_tags(self):
        return list(self.tags)

    def clear_tags(self):
        self.tags.clear()
        while self.chips_layout.count():
            item = self.chips_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()
        self.input.clear()

class StarRating(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rating = 3
        self.stars = []
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        for i in range(1, 6):
            btn = QPushButton("★")
            btn.setObjectName("star")
            btn.setFixedSize(32, 32)
            btn.clicked.connect(lambda _, v=i: self.set_rating(v))
            layout.addWidget(btn)
            self.stars.append(btn)
        layout.addStretch()
        self.set_rating(3)

    def set_rating(self, value):
        self._rating = value
        for i, btn in enumerate(self.stars):
            btn.setProperty("active", "true" if i < value else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    def get_rating(self):
        return self._rating

class FlowWidget(QWidget):
    def __init__(self, items, parent=None):
        super().__init__(parent)
        layout = FlowLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(6)
        for item in items:
            lbl = QLabel(item)
            lbl.setStyleSheet(f"""
                background: {TAG_BG}; color: {TAG_FG};
                border: 1px solid #4c2885; border-radius: 12px;
                padding: 3px 10px; font-size: 12px; font-weight: 500;
            """)
            layout.addWidget(lbl)
