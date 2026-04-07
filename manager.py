import sys
import json
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QComboBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QStackedWidget,
    QAbstractItemView,
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtWidgets import QLayout
from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QFont


DATA_FILE = "books.json"

# ── Palette ────────────────────────────────────────────────────────────────────
BG = "#0f0f13"
SURFACE = "#16161d"
SURFACE2 = "#1e1e28"
BORDER = "#2a2a38"
ACCENT = "#c084fc"  # lavender-purple
ACCENT2 = "#f472b6"  # pink
TEXT = "#e8e8f0"
TEXT_DIM = "#7a7a96"
TAG_BG = "#2d1f4e"
TAG_FG = "#c084fc"
SUCCESS = "#4ade80"
WARNING = "#fb923c"

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


# ── Tag Chip ───────────────────────────────────────────────────────────────────
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


# ── Tag Input Widget ───────────────────────────────────────────────────────────
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


# ── Flow Layout ────────────────────────────────────────────────────────────────


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=6):
        super().__init__(parent)
        self._items = []
        self.setSpacing(spacing)
        if parent:
            self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), test_only=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, test_only=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        size += QSize(m.left() + m.right(), m.top() + m.bottom())
        return size

    def _do_layout(self, rect, test_only):
        m = self.contentsMargins()
        x = rect.x() + m.left()
        y = rect.y() + m.top()
        line_height = 0
        spacing = self.spacing()

        for item in self._items:
            # w = item.widget()
            space_x = spacing
            space_y = spacing
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() - m.right() and line_height > 0:
                x = rect.x() + m.left()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0
            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y() + m.bottom()


# ── Star Rating Widget ─────────────────────────────────────────────────────────
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


# ── Section Header ─────────────────────────────────────────────────────────────
def section_label(text):
    lbl = QLabel(text.upper())
    lbl.setObjectName("section_title")
    return lbl


# ── Labeled Field helper ───────────────────────────────────────────────────────
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


# ── Book Detail Panel ──────────────────────────────────────────────────────────
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"books": []}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ── Main App ───────────────────────────────────────────────────────────────────
class BookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Manager")
        self.resize(1100, 720)
        self.setMinimumSize(880, 560)
        self.data = load_data()
        self._build_ui()
        self.refresh_list()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(16, 20, 16, 16)
        sb_layout.setSpacing(12)

        # Header
        header_row = QHBoxLayout()
        title = QLabel("📚 Library")
        title.setObjectName("app_title")
        header_row.addWidget(title)
        header_row.addStretch()
        add_btn = QPushButton("＋ New")
        add_btn.setObjectName("primary")
        add_btn.setFixedHeight(34)
        add_btn.setStyleSheet("""
            QPushButton#primary {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #8b5cf6,stop:1 #f472b6);
                border: none; color: white; font-weight: 600;
                font-size: 13px; padding: 6px 14px; border-radius: 8px;
            }
            QPushButton#primary:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7c3aed,stop:1 #ec4899);
            }
        """)
        add_btn.clicked.connect(self.show_add_form)
        header_row.addWidget(add_btn)
        sb_layout.addLayout(header_row)

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search books…")
        self.search_input.textChanged.connect(self.filter_list)
        sb_layout.addWidget(self.search_input)

        # Count
        self.count_label = QLabel()
        self.count_label.setObjectName("book_count")
        sb_layout.addWidget(self.count_label)

        # Book list
        self.book_list = QListWidget()
        self.book_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.book_list.currentRowChanged.connect(self.on_book_selected)
        sb_layout.addWidget(self.book_list)

        root.addWidget(sidebar)

        # ── Main panel (stacked) ──────────────────────────────────────────────
        self.stack = QStackedWidget()

        # Page 0: empty state
        empty = QWidget()
        el = QVBoxLayout(empty)
        el.setAlignment(Qt.AlignCenter)
        emoji = QLabel("📖")
        emoji.setStyleSheet("font-size: 56px;")
        emoji.setAlignment(Qt.AlignCenter)
        hint = QLabel("Select a book or add a new one")
        hint.setStyleSheet(f"color: {TEXT_DIM}; font-size: 15px;")
        hint.setAlignment(Qt.AlignCenter)
        el.addWidget(emoji)
        el.addWidget(hint)
        self.stack.addWidget(empty)  # index 0

        # Page 1: add/edit form
        self.form_page = self._build_form_page()
        self.stack.addWidget(self.form_page)  # index 1

        # Page 2: book detail
        self.detail_page = self._build_detail_page()
        self.stack.addWidget(self.detail_page)  # index 2

        root.addWidget(self.stack, 1)

    # ── Form page ─────────────────────────────────────────────────────────────
    def _build_form_page(self):
        outer = QWidget()
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(32, 28, 32, 32)
        layout.setSpacing(6)

        # Title bar
        self.form_title_label = QLabel("Add New Book")
        self.form_title_label.setStyleSheet(
            f"font-size: 20px; font-weight: 700; color: {TEXT}; margin-bottom: 4px;"
        )
        layout.addWidget(self.form_title_label)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        layout.addWidget(divider)
        layout.addSpacing(8)

        # ── Book info section ──────────────────────────────────────────────
        layout.addWidget(section_label("Book Info"))
        layout.addSpacing(4)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book title")
        layout.addLayout(labeled_row("Title *", self.title_input))

        self.authors_tag = TagInputWidget("Type author name + Enter")
        layout.addLayout(labeled_row("Authors", self.authors_tag))

        row2 = QHBoxLayout()
        row2.setSpacing(12)
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("e.g. 2023")
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("e.g. 320")
        row2.addWidget(self.year_input)
        row2.addWidget(self.pages_input)
        year_pages = QWidget()
        year_pages.setLayout(row2)
        layout.addLayout(labeled_row("Year / Pages", year_pages))

        self.publisher_input = QLineEdit()
        self.publisher_input.setPlaceholderText("Publisher name")
        layout.addLayout(labeled_row("Publisher", self.publisher_input))

        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("e.g. English")
        layout.addLayout(labeled_row("Language", self.language_input))

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN-13")
        layout.addLayout(labeled_row("ISBN", self.isbn_input))

        layout.addSpacing(14)
        divider2 = QFrame()
        divider2.setObjectName("divider")
        divider2.setFixedHeight(1)
        layout.addWidget(divider2)
        layout.addSpacing(8)

        # ── Classification ──────────────────────────────────────────────────
        layout.addWidget(section_label("Classification"))
        layout.addSpacing(4)

        self.categories_tag = TagInputWidget("Type category + Enter")
        layout.addLayout(labeled_row("Categories", self.categories_tag))

        self.tags_tag = TagInputWidget("Type tag + Enter")
        layout.addLayout(labeled_row("Tags", self.tags_tag))

        layout.addSpacing(14)
        divider3 = QFrame()
        divider3.setObjectName("divider")
        divider3.setFixedHeight(1)
        layout.addWidget(divider3)
        layout.addSpacing(8)

        # ── Reading status ──────────────────────────────────────────────────
        layout.addWidget(section_label("Reading Status"))
        layout.addSpacing(4)

        status_row = QHBoxLayout()
        status_row.setSpacing(8)
        self.status_btns = {}
        for s, icon in [
            ("unread", "○  Unread"),
            ("reading", "◑  Reading"),
            ("read", "●  Read"),
        ]:
            btn = QPushButton(icon)
            btn.setCheckable(True)
            btn.setProperty("status_val", s)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {SURFACE2}; border: 1px solid {BORDER};
                    border-radius: 8px; padding: 7px 14px; color: {TEXT_DIM};
                    font-size: 12px; font-weight: 500;
                }}
                QPushButton:checked {{
                    background: {TAG_BG}; border-color: {ACCENT}; color: {ACCENT};
                    font-weight: 600;
                }}
                QPushButton:hover:!checked {{ border-color: {TEXT_DIM}; color: {TEXT}; }}
            """)
            btn.clicked.connect(lambda _, b=btn: self._select_status(b))
            status_row.addWidget(btn)
            self.status_btns[s] = btn
        status_row.addStretch()
        sw = QWidget()
        sw.setLayout(status_row)
        layout.addLayout(labeled_row("Status", sw))
        self.status_btns["unread"].setChecked(True)

        layout.addLayout(labeled_row("Rating", self._make_rating_widget()))

        self.source_combo = QComboBox()
        self.source_combo.addItems(
            ["purchased", "gift", "found", "borrowed", "digital"]
        )
        layout.addLayout(labeled_row("Source", self.source_combo))

        layout.addSpacing(14)
        divider4 = QFrame()
        divider4.setObjectName("divider")
        divider4.setFixedHeight(1)
        layout.addWidget(divider4)
        layout.addSpacing(8)

        # ── Links & Notes ──────────────────────────────────────────────────
        layout.addWidget(section_label("Links & Notes"))
        layout.addSpacing(4)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://…")
        layout.addLayout(labeled_row("URL", self.url_input))

        self.image_url_input = QLineEdit()
        self.image_url_input.setPlaceholderText("Cover image URL")
        layout.addLayout(labeled_row("Cover URL", self.image_url_input))

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Personal notes, quotes, thoughts…")
        self.notes_input.setMinimumHeight(100)
        self.notes_input.setMaximumHeight(160)
        layout.addLayout(labeled_row("Notes", self.notes_input))

        layout.addSpacing(20)

        # ── Action buttons ─────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        self.save_btn = QPushButton("Save Book")
        self.save_btn.setObjectName("primary")
        self.save_btn.setMinimumWidth(130)
        self.save_btn.clicked.connect(self.save_book)
        btn_row.addWidget(self.save_btn)
        layout.addLayout(btn_row)

        scroll.setWidget(inner)
        outer_layout.addWidget(scroll)
        return outer

    def _make_rating_widget(self):
        self.star_rating = StarRating()
        return self.star_rating

    def _select_status(self, clicked_btn):
        for btn in self.status_btns.values():
            btn.setChecked(False)
        clicked_btn.setChecked(True)

    # ── Detail page ────────────────────────────────────────────────────────────
    def _build_detail_page(self):
        outer = QWidget()
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        self.detail_inner = QWidget()
        self.detail_layout = QVBoxLayout(self.detail_inner)
        self.detail_layout.setContentsMargins(32, 28, 32, 32)
        self.detail_layout.setSpacing(8)

        scroll.setWidget(self.detail_inner)
        outer_layout.addWidget(scroll)
        return outer

    def _populate_detail(self, book):
        # Clear old widgets
        while self.detail_layout.count():
            item = self.detail_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Title row
        top_row = QHBoxLayout()
        title_lbl = QLabel(book.get("title", "Untitled"))
        title_lbl.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {TEXT};")
        title_lbl.setWordWrap(True)
        top_row.addWidget(title_lbl, 1)

        edit_btn = QPushButton("✏️  Edit")
        edit_btn.clicked.connect(lambda: self.open_edit_form(book))
        top_row.addWidget(edit_btn)

        del_btn = QPushButton("🗑  Delete")
        del_btn.setObjectName("danger")
        del_btn.clicked.connect(lambda: self.delete_book(book))
        top_row.addWidget(del_btn)

        self.detail_layout.addLayout(top_row)

        # Authors
        authors = book.get("authors", [])
        if authors:
            a_lbl = QLabel(", ".join(authors))
            a_lbl.setStyleSheet(f"color: {ACCENT}; font-size: 14px; font-weight: 500;")
            self.detail_layout.addWidget(a_lbl)

        # Status + rating row
        sr_row = QHBoxLayout()
        sr_row.setSpacing(16)
        status = book.get("status", "unread")
        status_colors = {"unread": TEXT_DIM, "reading": WARNING, "read": SUCCESS}
        status_icons = {"unread": "○", "reading": "◑", "read": "●"}
        s_lbl = QLabel(f"{status_icons.get(status,'○')}  {status.capitalize()}")
        s_lbl.setStyleSheet(
            f"color: {status_colors.get(status, TEXT_DIM)}; font-weight: 600; font-size: 13px;"
        )
        sr_row.addWidget(s_lbl)

        rating = book.get("rating", 0)
        r_lbl = QLabel("★" * rating + "☆" * (5 - rating))
        r_lbl.setStyleSheet("color: #fbbf24; font-size: 16px; letter-spacing: 2px;")
        sr_row.addWidget(r_lbl)
        sr_row.addStretch()
        self.detail_layout.addLayout(sr_row)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        self.detail_layout.addWidget(divider)
        self.detail_layout.addSpacing(8)

        # Meta grid
        meta_fields = [
            ("Year", str(book.get("year", ""))),
            ("Pages", str(book.get("pages", ""))),
            ("Publisher", book.get("publisher", "")),
            ("Language", book.get("language", "")),
            ("ISBN", book.get("isbn", "")),
            ("Source", book.get("source", "")),
            ("Added", book.get("date_added", "")),
        ]
        for label, value in meta_fields:
            if value:
                row = QHBoxLayout()
                k = QLabel(label)
                k.setStyleSheet(f"color: {TEXT_DIM}; font-size: 12px; min-width: 80px;")
                v = QLabel(value)
                v.setStyleSheet(f"color: {TEXT}; font-size: 13px;")
                row.addWidget(k)
                row.addWidget(v, 1)
                self.detail_layout.addLayout(row)

        # Tags / categories
        for field_name, field_key in [("Categories", "categories"), ("Tags", "tags")]:
            items = book.get(field_key, [])
            if items:
                self.detail_layout.addSpacing(4)
                fl = QLabel(field_name)
                fl.setObjectName("section_title")
                self.detail_layout.addWidget(fl)
                chip_row = FlowWidget(items)
                self.detail_layout.addWidget(chip_row)

        # URL
        url = book.get("url", "")
        if url:
            self.detail_layout.addSpacing(4)
            url_lbl = QLabel(f'<a href="{url}" style="color:{ACCENT}">{url}</a>')
            url_lbl.setOpenExternalLinks(True)
            self.detail_layout.addWidget(url_lbl)

        # Notes
        notes = book.get("notes", "")
        if notes:
            self.detail_layout.addSpacing(8)
            n_title = QLabel("NOTES")
            n_title.setObjectName("section_title")
            self.detail_layout.addWidget(n_title)
            n_lbl = QLabel(notes)
            n_lbl.setWordWrap(True)
            n_lbl.setStyleSheet(f"""
                color: {TEXT_DIM}; font-size: 13px; line-height: 1.6;
                background: {SURFACE2}; border-radius: 8px;
                padding: 12px; border: 1px solid {BORDER};
            """)
            self.detail_layout.addWidget(n_lbl)

        self.detail_layout.addStretch()

    # ── FlowWidget for read-only chips ──────────────────────────────────────
    # (inline below)

    # ── List management ────────────────────────────────────────────────────────
    def refresh_list(self):
        query = (
            self.search_input.text().lower() if hasattr(self, "search_input") else ""
        )
        self.book_list.clear()
        filtered = [
            b
            for b in self.data["books"]
            if query in b.get("title", "").lower()
            or any(query in a.lower() for a in b.get("authors", []))
        ]
        for book in filtered:
            status = book.get("status", "unread")
            icons = {"unread": "○", "reading": "◑", "read": "●"}
            item = QListWidgetItem(f'{icons.get(status,"○")}  {book["title"]}')
            item.setData(Qt.UserRole, book.get("id"))
            self.book_list.addItem(item)
        total = len(self.data["books"])
        shown = len(filtered)
        self.count_label.setText(f"{shown} of {total} book{'s' if total != 1 else ''}")

    def filter_list(self):
        self.refresh_list()

    def on_book_selected(self, row):
        if row < 0:
            return
        item = self.book_list.item(row)
        if not item:
            return
        book_id = item.data(Qt.UserRole)
        book = next((b for b in self.data["books"] if b.get("id") == book_id), None)
        if book:
            self._populate_detail(book)
            self.stack.setCurrentIndex(2)

    # ── Forms ──────────────────────────────────────────────────────────────────
    def show_add_form(self):
        self._editing_id = None
        self.form_title_label.setText("Add New Book")
        self.save_btn.setText("Save Book")
        self._clear_form()
        self.stack.setCurrentIndex(1)

    def open_edit_form(self, book):
        self._editing_id = book.get("id")
        self.form_title_label.setText("Edit Book")
        self.save_btn.setText("Update Book")
        self._fill_form(book)
        self.stack.setCurrentIndex(1)

    def _fill_form(self, book):
        self._clear_form()
        self.title_input.setText(book.get("title", ""))
        for a in book.get("authors", []):
            self.authors_tag.add_tag(a)
        self.year_input.setText(str(book.get("year", "")))
        self.pages_input.setText(str(book.get("pages", "")))
        self.publisher_input.setText(book.get("publisher", ""))
        self.language_input.setText(book.get("language", ""))
        self.isbn_input.setText(book.get("isbn", ""))
        for c in book.get("categories", []):
            self.categories_tag.add_tag(c)
        for t in book.get("tags", []):
            self.tags_tag.add_tag(t)
        status = book.get("status", "unread")
        for s, btn in self.status_btns.items():
            btn.setChecked(s == status)
        self.star_rating.set_rating(book.get("rating", 3))
        src = book.get("source", "purchased")
        idx = self.source_combo.findText(src)
        if idx >= 0:
            self.source_combo.setCurrentIndex(idx)
        self.url_input.setText(book.get("url", "") or "")
        self.image_url_input.setText(book.get("image_url", "") or "")
        self.notes_input.setPlainText(book.get("notes", ""))

    def _clear_form(self):
        self.title_input.clear()
        self.authors_tag.clear_tags()
        self.year_input.clear()
        self.pages_input.clear()
        self.publisher_input.clear()
        self.language_input.clear()
        self.isbn_input.clear()
        self.categories_tag.clear_tags()
        self.tags_tag.clear_tags()
        for btn in self.status_btns.values():
            btn.setChecked(False)
        self.status_btns["unread"].setChecked(True)
        self.star_rating.set_rating(3)
        self.source_combo.setCurrentIndex(0)
        self.url_input.clear()
        self.image_url_input.clear()
        self.notes_input.clear()

    def save_book(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation", "Title is required.")
            return

        status = next(
            (s for s, btn in self.status_btns.items() if btn.isChecked()), "unread"
        )

        try:
            year = int(self.year_input.text()) if self.year_input.text().strip() else 0
            pages = (
                int(self.pages_input.text()) if self.pages_input.text().strip() else 0
            )
        except ValueError:
            QMessageBox.warning(self, "Validation", "Year and Pages must be numbers.")
            return

        book_data = {
            "title": title,
            "authors": self.authors_tag.get_tags(),
            "year": year,
            "publisher": self.publisher_input.text(),
            "language": self.language_input.text(),
            "isbn": self.isbn_input.text(),
            "pages": pages,
            "categories": self.categories_tag.get_tags(),
            "tags": self.tags_tag.get_tags(),
            "status": status,
            "rating": self.star_rating.get_rating(),
            "source": self.source_combo.currentText(),
            "url": self.url_input.text() or None,
            "image_url": self.image_url_input.text() or None,
            "notes": self.notes_input.toPlainText(),
            "date_added": datetime.now().strftime("%Y-%m-%d"),
            "date_read": "",
        }

        if self._editing_id:
            for i, b in enumerate(self.data["books"]):
                if b.get("id") == self._editing_id:
                    book_data["id"] = self._editing_id
                    book_data["date_added"] = b.get(
                        "date_added", book_data["date_added"]
                    )
                    self.data["books"][i] = book_data
                    break
        else:
            book_data["id"] = f"book_{len(self.data['books']) + 1:03d}"
            self.data["books"].append(book_data)

        save_data(self.data)
        self.refresh_list()
        self._populate_detail(book_data)
        self.stack.setCurrentIndex(2)

    def delete_book(self, book):
        reply = QMessageBox.question(
            self,
            "Delete Book",
            f'Delete "{book.get("title", "this book")}"?',
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.data["books"] = [
                b for b in self.data["books"] if b.get("id") != book.get("id")
            ]
            save_data(self.data)
            self.refresh_list()
            self.stack.setCurrentIndex(0)


# ── Read-only chip row ─────────────────────────────────────────────────────────
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


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    # App-level font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = BookApp()
    window.show()
    sys.exit(app.exec_())
