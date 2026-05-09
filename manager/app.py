import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QListWidget, QListWidgetItem, QMessageBox, QComboBox,
    QScrollArea, QFrame, QStackedWidget, QAbstractItemView
)
from PyQt5.QtCore import Qt

from .constants import TEXT, TEXT_DIM, ACCENT, WARNING, SUCCESS, TAG_BG
from .data_manager import load_data, save_data
from .widgets import TagInputWidget, StarRating, FlowWidget
from .utils import section_label, labeled_row

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
                    background: {TAG_BG}; border: 1px solid {TAG_BG}; /* Replaced SURFACE2 with TAG_BG for better visual consistency */
                    border-radius: 8px; padding: 7px 14px; color: {TEXT_DIM};
                    font-size: 12px; font-weight: 500;
                }}
                QPushButton:checked {{
                    background: {TAG_BG}; border-color: {ACCENT}; color: {ACCENT};
                    font-weight: 600;
                }}
                QPushButton:hover:!checked {{ border-color: {TEXT_DIM}; color: {TEXT}; }}
            """)
            # Note: I noticed SURFACE2 was used in original, let's stick to original or constants
            # Actually original used SURFACE2 which is defined in constants.
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: #1e1e28; border: 1px solid #2a2a38;
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
        self._clear_layout(self.detail_layout)

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
                background: #1e1e28; border-radius: 8px;
                padding: 12px; border: 1px solid #2a2a38;
            """)
            self.detail_layout.addWidget(n_lbl)

        self.detail_layout.addStretch()

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

    def _clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self._clear_layout(item.layout())
