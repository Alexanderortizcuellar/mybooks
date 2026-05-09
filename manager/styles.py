from .constants import (
    BG, SURFACE, SURFACE2, BORDER, ACCENT, ACCENT2, TEXT, TEXT_DIM, TAG_BG, SUCCESS, WARNING
)

STYLESHEET = f"""
QWidget {{
    background: {BG};
    color: {TEXT};
    font-family: "Segoe UI", "SF Pro Display", sans-serif;
    font-size: 13px;
}}

/* ── Scrollbar ── */
QScrollBar:vertical {{
    background: {SURFACE};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

QScrollBar:horizontal {{
    background: {SURFACE};
    height: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER};
    border-radius: 3px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}

/* ── Inputs ── */
QLineEdit {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {TEXT};
    selection-background-color: {ACCENT};
}}
QLineEdit:focus {{
    border: 1px solid {ACCENT};
    background: #1c1c28;
}}
QLineEdit::placeholder {{
    color: {TEXT_DIM};
}}

QTextEdit {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {TEXT};
}}
QTextEdit:focus {{
    border: 1px solid {ACCENT};
}}

QComboBox {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: {TEXT};
    min-width: 120px;
}}
QComboBox:focus {{
    border: 1px solid {ACCENT};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {TEXT_DIM};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    selection-background-color: {ACCENT};
    color: {TEXT};
    outline: none;
}}

/* ── Buttons ── */
QPushButton {{
    background: {SURFACE2};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 16px;
    color: {TEXT};
    font-weight: 500;
}}
QPushButton:hover {{
    background: {SURFACE};
    border-color: {ACCENT};
    color: {ACCENT};
}}
QPushButton:pressed {{
    background: {TAG_BG};
}}

QPushButton#primary {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #8b5cf6, stop:1 {ACCENT2});
    border: none;
    color: white;
    font-weight: 600;
    font-size: 14px;
    padding: 11px 24px;
    border-radius: 10px;
}}
QPushButton#primary:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c3aed, stop:1 #ec4899);
}}
QPushButton#primary:pressed {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #6d28d9, stop:1 #db2777);
}}

QPushButton#danger {{
    background: transparent;
    border: 1px solid #7f1d1d;
    color: #f87171;
    border-radius: 8px;
    padding: 7px 14px;
    font-size: 12px;
}}
QPushButton#danger:hover {{
    background: #7f1d1d44;
    border-color: #f87171;
}}

QPushButton#icon_btn {{
    background: transparent;
    border: none;
    color: {TEXT_DIM};
    padding: 4px;
    border-radius: 4px;
    font-size: 16px;
}}
QPushButton#icon_btn:hover {{
    color: {TEXT};
    background: {SURFACE2};
}}

/* ── List ── */
QListWidget {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 4px;
    outline: none;
}}
QListWidget::item {{
    border-radius: 8px;
    padding: 10px 14px;
    margin: 1px 2px;
    color: {TEXT};
}}
QListWidget::item:selected {{
    background: {TAG_BG};
    color: {ACCENT};
    border-left: 3px solid {ACCENT};
}}
QListWidget::item:hover:!selected {{
    background: {SURFACE2};
}}

/* ── Labels ── */
QLabel#section_title {{
    font-size: 11px;
    font-weight: 600;
    color: {TEXT_DIM};
    letter-spacing: 1.5px;
    padding: 0;
    text-transform: uppercase;
}}
QLabel#app_title {{
    font-size: 22px;
    font-weight: 700;
    color: {TEXT};
    letter-spacing: -0.5px;
}}
QLabel#book_count {{
    font-size: 12px;
    color: {TEXT_DIM};
}}
QLabel#form_label {{
    color: {TEXT_DIM};
    font-size: 12px;
    font-weight: 500;
    min-width: 90px;
}}

/* ── Frames ── */
QFrame#card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 12px;
}}
QFrame#divider {{
    background: {BORDER};
    max-height: 1px;
}}
QFrame#sidebar {{
    background: {SURFACE};
    border-right: 1px solid {BORDER};
}}

/* ── Star rating ── */
QPushButton#star {{
    background: transparent;
    border: none;
    color: #3a3a4e;
    font-size: 22px;
    padding: 2px;
}}
QPushButton#star[active="true"] {{
    color: #fbbf24;
}}
QPushButton#star:hover {{
    color: #fcd34d;
}}
"""
