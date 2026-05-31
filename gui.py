"""
gui.py
Графички кориснички интерфејс (GUI) — PyQt5
Содржи: MainWindow, RecommendPage, DatabasePage, StatsPage
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QScrollArea, QFrame,
    QLineEdit, QGraphicsDropShadowEffect,
    QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QFormLayout, QDialogButtonBox, QSpinBox,
    QDoubleSpinBox, QSlider, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from knowledge_base import CATEGORIES, NAMENI, CAT_ICONS
from inference_engine import preporacaj
from database import db_all, db_add, db_delete, db_stats

# ═══════════════════════════════════════════════════════════════════
#  СТИЛОВИ
# ═══════════════════════════════════════════════════════════════════

QSS = """
* { font-family: 'Segoe UI', sans-serif; }
QMainWindow, QWidget { background: #0d1018; color: #dde1f0; }
QWidget#sidebar { background: #10131c; border-right: 1px solid #1c2030; }
QPushButton#nav {
    background: transparent; border: none; border-radius: 10px;
    padding: 13px 20px; text-align: left; font-size: 14px;
    color: #5a6080; font-weight: 500;
}
QPushButton#nav:hover { background: #181d2c; color: #a0aacc; }
QPushButton#nav[active=true] {
    background: #192340; color: #60aaff;
    border-left: 3px solid #4080e0; font-weight: 600;
}
QFrame#panel { background: #141824; border: 1px solid #1e2538; border-radius: 16px; }
QFrame#resultCard { background: #141824; border: 1px solid #1e2a40; border-radius: 14px; }
QFrame#resultCard:hover { border: 1px solid #3060b0; }
QFrame#topCard { background: #192040; border: 1px solid #2e55a8; border-radius: 14px; }
QComboBox {
    background: #181e30; border: 1px solid #252e48;
    border-radius: 10px; padding: 10px 16px;
    font-size: 14px; color: #b8c0dc; min-height: 22px;
}
QComboBox:focus { border-color: #4080e0; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox::down-arrow {
    width: 0; height: 0;
    border-left: 5px solid transparent; border-right: 5px solid transparent;
    border-top: 6px solid #4080e0; margin-right: 10px;
}
QComboBox QAbstractItemView {
    background: #181e30; border: 1px solid #303a58;
    selection-background-color: #263558; color: #b8c0dc; padding: 4px;
}
QSlider::groove:horizontal { height: 6px; background: #1e2840; border-radius: 3px; }
QSlider::handle:horizontal {
    background: #4080e0; width: 18px; height: 18px;
    margin: -6px 0; border-radius: 9px;
}
QSlider::sub-page:horizontal {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #2050b0,stop:1 #4090f0);
    border-radius: 3px;
}
QPushButton#searchBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #1e50c0,stop:1 #3a80f0);
    color: #fff; border: none; border-radius: 12px;
    padding: 14px 36px; font-size: 15px; font-weight: 700;
}
QPushButton#searchBtn:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #2a60d0,stop:1 #4a90ff);
}
QPushButton#searchBtn:pressed { background: #1840a0; }
QPushButton#addBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #165a38,stop:1 #22904e);
    color:#fff; border:none; border-radius:9px; padding:9px 20px; font-weight:600;
}
QPushButton#addBtn:hover { background: #28a85c; }
QPushButton#delBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #6a1212,stop:1 #962020);
    color:#fff; border:none; border-radius:9px; padding:9px 20px; font-weight:600;
}
QPushButton#delBtn:hover { background: #b83030; }
QTableWidget {
    background: #10131c; border: 1px solid #1e2538; border-radius: 12px;
    gridline-color: #1c2230; font-size: 13px; color: #b8c0dc;
    selection-background-color: #243060;
}
QTableWidget::item { padding: 8px 14px; border: none; }
QHeaderView::section {
    background: #181e30; color: #5a9af0; border: none;
    border-bottom: 1px solid #252e48; padding: 10px 14px;
    font-weight: 700; font-size: 11px; letter-spacing: 0.8px;
}
QScrollBar:vertical { background: #0d1018; width: 7px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #202840; border-radius: 4px; min-height: 24px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 0; }
QLineEdit, QSpinBox, QDoubleSpinBox {
    background: #181e30; border: 1px solid #252e48;
    border-radius: 8px; padding: 8px 12px; color: #b8c0dc; font-size: 13px;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus { border-color: #4080e0; }
QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: #252e48; border: none; width: 20px;
}
"""

# ═══════════════════════════════════════════════════════════════════
#  ПОМОШНИ ФУНКЦИИ
# ═══════════════════════════════════════════════════════════════════

def lbl(text, size=13, bold=False, color="#dde1f0", align=None):
    w = QLabel(text)
    f = QFont("Segoe UI", size); f.setBold(bold)
    w.setFont(f); w.setStyleSheet(f"color:{color};background:transparent;")
    if align: w.setAlignment(align)
    return w

def shadow_eff(widget):
    e = QGraphicsDropShadowEffect()
    e.setBlurRadius(24); e.setColor(QColor(0,0,0,120)); e.setOffset(0,4)
    widget.setGraphicsEffect(e)

def stars(r):
    full = int(r); half = 1 if r - full >= 0.5 else 0; empty = 5-full-half
    return "★"*full + ("⯨" if half else "") + "☆"*empty

# ═══════════════════════════════════════════════════════════════════
#  СТРАНА: ПРЕПОРАКА
# ═══════════════════════════════════════════════════════════════════

class RecommendPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28,22,28,18); root.setSpacing(18)

        hdr = QHBoxLayout()
        hdr.addWidget(lbl("🔍  Препорака на производи", 20, True, "#e0e6ff"))
        hdr.addStretch()
        hdr.addWidget(lbl("Системи базирани на знаење · 2026", 11, False, "#404868"))
        root.addLayout(hdr)

        panel = QFrame(); panel.setObjectName("panel")
        pgrid = QGridLayout(panel); pgrid.setContentsMargins(22,18,22,18); pgrid.setSpacing(14)
        shadow_eff(panel)

        pgrid.addWidget(lbl("Категорија", 12, True, "#5a9af0"), 0, 0)
        pgrid.addWidget(lbl("Намена", 12, True, "#5a9af0"), 0, 1)
        pgrid.addWidget(lbl("Макс. буџет (ден.)", 12, True, "#5a9af0"), 0, 2)
        pgrid.addWidget(lbl("Мин. рејтинг", 12, True, "#5a9af0"), 0, 3)

        self.cmbCat = QComboBox(); self.cmbCat.addItems(CATEGORIES)
        self.cmbNam = QComboBox(); self.cmbNam.addItems(NAMENI)

        self.sldPrice = QSlider(Qt.Horizontal)
        self.sldPrice.setRange(1000, 200000); self.sldPrice.setValue(100000)
        self.lblPrice = lbl("100.000 ден.", 12, False, "#a0b0d0")
        self.sldPrice.valueChanged.connect(
            lambda v: self.lblPrice.setText(f"{v:,} ден.".replace(",",".")))

        self.sldRating = QSlider(Qt.Horizontal)
        self.sldRating.setRange(0, 50); self.sldRating.setValue(0)
        self.lblRating = lbl("Сите  ★", 12, False, "#a0b0d0")
        self.sldRating.valueChanged.connect(
            lambda v: self.lblRating.setText(f"{v/10:.1f}  ★"))

        pgrid.addWidget(self.cmbCat, 1, 0)
        pgrid.addWidget(self.cmbNam, 1, 1)

        pv = QVBoxLayout(); pv.setSpacing(4)
        pv.addWidget(self.sldPrice); pv.addWidget(self.lblPrice)
        pgrid.addLayout(pv, 1, 2)

        rv = QVBoxLayout(); rv.setSpacing(4)
        rv.addWidget(self.sldRating); rv.addWidget(self.lblRating)
        pgrid.addLayout(rv, 1, 3)

        for c in range(4): pgrid.setColumnStretch(c, 1)
        root.addWidget(panel)

        btn = QPushButton("  🔎   Пребарај производи"); btn.setObjectName("searchBtn")
        btn.setCursor(Qt.PointingHandCursor); btn.clicked.connect(self._search)
        root.addWidget(btn)

        self.resLabel = lbl("", 13, False, "#5a6888")
        root.addWidget(self.resLabel)

        scroll = QScrollArea(); scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        self.resContainer = QWidget()
        self.resLayout = QVBoxLayout(self.resContainer)
        self.resLayout.setSpacing(10); self.resLayout.setContentsMargins(0,0,0,0)
        self.resLayout.addStretch()
        scroll.setWidget(self.resContainer)
        root.addWidget(scroll, 1)

    def _search(self):
        cat  = self.cmbCat.currentText()
        nam  = self.cmbNam.currentText()
        maxp = self.sldPrice.value()
        minr = self.sldRating.value() / 10
        rows = preporacaj(cat, nam, maxp, minr)   # <- Inference Engine

        while self.resLayout.count() > 1:
            item = self.resLayout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        if not rows:
            self.resLabel.setText("❌  Нема производи кои ги исполнуваат критериумите.")
            self.resLabel.setStyleSheet("color:#b04040;background:transparent;")
            return

        self.resLabel.setText(f"✅  Пронајдени {len(rows)} производ(и) · сортирани по рејтинг")
        self.resLabel.setStyleSheet("color:#40b870;background:transparent;")

        for i, row in enumerate(rows):
            self.resLayout.insertWidget(i, self._make_card(row, top=(i==0)))

    def _make_card(self, row, top=False):
        pid, name, cat, brand, price, rating, nameni, desc = row
        icon = CAT_ICONS.get(cat, "📦")

        frame = QFrame(); frame.setObjectName("topCard" if top else "resultCard")
        shadow_eff(frame)

        h = QHBoxLayout(frame); h.setContentsMargins(18,14,18,14); h.setSpacing(16)

        ico = lbl(icon, 26, False, "#ffffff", Qt.AlignCenter)
        ico.setFixedSize(52,52)
        ico.setStyleSheet("background:#1a2540;border-radius:12px;color:#fff;")
        h.addWidget(ico)

        info = QVBoxLayout(); info.setSpacing(4)
        row1 = QHBoxLayout(); row1.setSpacing(10)
        row1.addWidget(lbl(name, 14, True, "#e0e8ff"))
        if top:
            badge = lbl("  🏆 ТОП  ", 10, True, "#f0c040")
            badge.setStyleSheet("background:#2a2000;border-radius:6px;padding:2px 8px;color:#f0c040;")
            row1.addWidget(badge)
        row1.addStretch()
        info.addLayout(row1)
        info.addWidget(lbl(f"{brand}  ·  {cat}  ·  {desc}", 12, False, "#606888"))
        info.addWidget(lbl(f"{stars(rating)}  {rating}/5.0  ·  {nameni.replace(',','  ·  ')}", 12, False, "#d0a020"))
        h.addLayout(info, 1)

        pblock = QVBoxLayout(); pblock.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        pblock.addWidget(lbl(f"{price:,} ден.".replace(",","."), 17, True, "#60b8ff", Qt.AlignRight))
        h.addLayout(pblock)

        return frame

# ═══════════════════════════════════════════════════════════════════
#  СТРАНА: БАЗА НА ПРОИЗВОДИ
# ═══════════════════════════════════════════════════════════════════

class DatabasePage(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(28,22,28,18); root.setSpacing(14)

        hdr = QHBoxLayout()
        hdr.addWidget(lbl("🗄  База на производи", 20, True, "#e0e6ff"))
        hdr.addStretch()
        addBtn = QPushButton("  ＋  Додај производ"); addBtn.setObjectName("addBtn")
        addBtn.setCursor(Qt.PointingHandCursor); addBtn.clicked.connect(self._add_dialog)
        delBtn = QPushButton("  🗑  Избриши избран"); delBtn.setObjectName("delBtn")
        delBtn.setCursor(Qt.PointingHandCursor); delBtn.clicked.connect(self._delete_selected)
        hdr.addWidget(addBtn); hdr.addWidget(delBtn)
        root.addLayout(hdr)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID","Назив","Категорија","Бренд","Цена (ден.)","Рејтинг","Намени","Опис"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(self.table.styleSheet() +
            "QTableWidget {alternate-background-color: #12161f;}")
        root.addWidget(self.table, 1)
        self.refresh()

    def refresh(self):
        rows = db_all()
        self.table.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                item = QTableWidgetItem(str(val) if val is not None else "")
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                if c == 4:
                    item.setText(f"{int(val):,}".replace(",","."))
                    item.setForeground(QColor("#60b8ff"))
                if c == 5:
                    item.setForeground(QColor("#d0a020"))
                self.table.setItem(r, c, item)
            self.table.setRowHeight(r, 38)

    def _add_dialog(self):
        dlg = QDialog(self); dlg.setWindowTitle("Додај нов производ")
        dlg.setStyleSheet("QDialog{background:#10131c;} QLabel{color:#dde1f0;}")
        dlg.resize(460, 400)
        form = QFormLayout(dlg); form.setSpacing(12); form.setContentsMargins(20,20,20,20)

        fields = {}
        def field(key, widget):
            fields[key] = widget; return widget

        form.addRow(lbl("Назив:", 12, True), field("name", QLineEdit()))
        cmbC = QComboBox(); cmbC.addItems(CATEGORIES[1:])
        form.addRow(lbl("Категорија:", 12, True), field("cat", cmbC))
        form.addRow(lbl("Бренд:", 12, True), field("brand", QLineEdit()))
        sp = QSpinBox(); sp.setRange(100, 999999); sp.setValue(30000)
        form.addRow(lbl("Цена (ден.):", 12, True), field("price", sp))
        rt = QDoubleSpinBox(); rt.setRange(1.0, 5.0); rt.setSingleStep(0.1); rt.setValue(4.0)
        form.addRow(lbl("Рејтинг:", 12, True), field("rating", rt))
        cmbN = QComboBox(); cmbN.addItems(NAMENI[1:])
        form.addRow(lbl("Намена:", 12, True), field("namena", cmbN))
        form.addRow(lbl("Опис:", 12, True), field("desc", QLineEdit()))

        btns = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btns.accepted.connect(dlg.accept); btns.rejected.connect(dlg.reject)
        btns.setStyleSheet("QPushButton{background:#1e3060;color:#fff;border:none;border-radius:7px;padding:8px 20px;}")
        form.addRow(btns)

        if dlg.exec_() == QDialog.Accepted:
            db_add(
                fields["name"].text(), fields["cat"].currentText(),
                fields["brand"].text(), fields["price"].value(),
                fields["rating"].value(), fields["namena"].currentText(),
                fields["desc"].text()
            )
            self.refresh()

    def _delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Грешка", "Избери производ за бришење!")
            return
        pid  = int(self.table.item(row, 0).text())
        name = self.table.item(row, 1).text()
        reply = QMessageBox.question(self, "Потврди бришење",
            f"Дали сигурно сакаш да го избришеш:\n{name}?",
            QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            db_delete(pid); self.refresh()

# ═══════════════════════════════════════════════════════════════════
#  СТРАНА: СТАТИСТИКА
# ═══════════════════════════════════════════════════════════════════

class StatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        root = QVBoxLayout(self); root.setContentsMargins(28,22,28,18); root.setSpacing(16)
        root.addWidget(lbl("📊  Статистика", 20, True, "#e0e6ff"))
        self.grid = QGridLayout(); self.grid.setSpacing(14)
        root.addLayout(self.grid)
        root.addStretch()
        self.refresh()

    def refresh(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w: w.deleteLater()

        s = db_stats()

        def stat_card(icon, title, value, color="#60b8ff"):
            f = QFrame(); f.setObjectName("panel"); shadow_eff(f)
            v = QVBoxLayout(f); v.setContentsMargins(20,16,20,16); v.setSpacing(6)
            v.addWidget(lbl(icon, 24, False, color, Qt.AlignCenter))
            v.addWidget(lbl(value, 22, True, color, Qt.AlignCenter))
            v.addWidget(lbl(title, 11, False, "#4a5878", Qt.AlignCenter))
            return f

        self.grid.addWidget(stat_card("🗄", "Вкупно производи", str(s["total"]), "#60b8ff"), 0, 0)
        self.grid.addWidget(stat_card("💰", "Просечна цена", f"{int(s['avg_price']):,} ден.".replace(",","."), "#50d090"), 0, 1)
        self.grid.addWidget(stat_card("⭐", "Просечен рејтинг", f"{s['avg_rating']:.2f} / 5.0", "#d0a020"), 0, 2)
        self.grid.addWidget(stat_card("📦", "Категории", str(len(s["categories"])), "#c060f0"), 0, 3)

        cat_frame = QFrame(); cat_frame.setObjectName("panel"); shadow_eff(cat_frame)
        cv = QVBoxLayout(cat_frame); cv.setContentsMargins(20,16,20,16); cv.setSpacing(10)
        cv.addWidget(lbl("Производи по категорија", 14, True, "#7090d0"))
        for cat, count in sorted(s["categories"], key=lambda x: -x[1]):
            rw = QWidget(); rh = QHBoxLayout(rw); rh.setContentsMargins(0,0,0,0)
            rh.addWidget(lbl(f"{CAT_ICONS.get(cat,'📦')}  {cat}", 13, False, "#b0bad8"))
            rh.addStretch()
            bar = QFrame(); bar.setFixedHeight(8)
            bar.setFixedWidth(int(count / s["total"] * 180))
            bar.setStyleSheet("background:#2a50a0;border-radius:4px;")
            rh.addWidget(bar)
            rh.addWidget(lbl(f"  {count}", 13, True, "#4080e0"))
            cv.addWidget(rw)
        self.grid.addWidget(cat_frame, 1, 0, 1, 2)

        top_frame = QFrame(); top_frame.setObjectName("panel"); shadow_eff(top_frame)
        tv = QVBoxLayout(top_frame); tv.setContentsMargins(20,16,20,16); tv.setSpacing(10)
        tv.addWidget(lbl("🏆  Врвни производи", 14, True, "#7090d0"))
        medals = ["🥇","🥈","🥉"]
        for i,(name,rat) in enumerate(s["top3"]):
            rw = QWidget(); rh = QHBoxLayout(rw); rh.setContentsMargins(0,0,0,0)
            rh.addWidget(lbl(f"{medals[i]}  {name}", 13, False, "#c0cadf"))
            rh.addStretch()
            rh.addWidget(lbl(f"{rat:.1f} ★", 13, True, "#d0a020"))
            tv.addWidget(rw)
        self.grid.addWidget(top_frame, 1, 2, 1, 2)

# ═══════════════════════════════════════════════════════════════════
#  ГЛАВЕН ПРОЗОРЕЦ
# ═══════════════════════════════════════════════════════════════════

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Систем за препорака на производи  ·  КБС 2026")
        self.resize(1100, 720); self.setMinimumSize(900, 620)

        central = QWidget(); self.setCentralWidget(central)
        layout = QHBoxLayout(central); layout.setContentsMargins(0,0,0,0); layout.setSpacing(0)

        sidebar = QWidget(); sidebar.setObjectName("sidebar"); sidebar.setFixedWidth(200)
        sv = QVBoxLayout(sidebar); sv.setContentsMargins(12,20,12,20); sv.setSpacing(4)

        logo = lbl("  🛒", 28, False, "#4080e0"); logo.setFixedHeight(48)
        sv.addWidget(logo)
        sv.addWidget(lbl("  Систем за\n  Препорака", 11, False, "#3a4868"))
        sv.addSpacing(20)

        self.nav_btns = []
        for i, title in enumerate(["🔍  Препорака", "🗄  База", "📊  Статистика"]):
            btn = QPushButton(title); btn.setObjectName("nav")
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda _, idx=i: self._switch(idx))
            sv.addWidget(btn); self.nav_btns.append(btn)

        sv.addStretch()
        sv.addWidget(lbl("  v2.0  ·  SQLite", 10, False, "#2a3050"))
        layout.addWidget(sidebar)

        self.pages = QStackedWidget()
        self.recPage  = RecommendPage()
        self.dbPage   = DatabasePage()
        self.statPage = StatsPage()
        for p in [self.recPage, self.dbPage, self.statPage]:
            self.pages.addWidget(p)
        layout.addWidget(self.pages, 1)
        self._switch(0)

    def _switch(self, idx):
        self.pages.setCurrentIndex(idx)
        for i, btn in enumerate(self.nav_btns):
            btn.setProperty("active", "true" if i == idx else "false")
            btn.style().unpolish(btn); btn.style().polish(btn)
        if idx == 1: self.dbPage.refresh()
        if idx == 2: self.statPage.refresh()


def start_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
