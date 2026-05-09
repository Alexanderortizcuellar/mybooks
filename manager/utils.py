from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from .constants import TEXT_DIM

def section_label(text):
    lbl = QLabel(text.upper())
    lbl.setObjectName("section_title")
    return lbl

def labeled_row(label_text, widget):
    row = QHBoxLayout()
    row.setSpacing(12)
    lbl = QLabel(label_text)
    lbl.setObjectName("form_label")
    lbl.setFixedWidth(95)
    lbl.setAlignment(Qt.AlignTop | Qt.AlignRight)
    lbl.setStyleSheet(f"color: {TEXT_DIM}; font-size: 12px; padding-top: 8px;")
    row.addWidget(lbl)
    row.addWidget(widget, 1)
    return row
