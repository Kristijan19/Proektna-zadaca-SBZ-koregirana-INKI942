"""
database.py
Слој за работа со SQLite базата на податоци.
Содржи: иницијализација, читање, додавање и бришење на производи.
"""

import sqlite3, os
from knowledge_base import SEED

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.db")


def init_db():
    """Креира ја базата и ја пополнува со seed data ако е празна."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,
            brand       TEXT NOT NULL,
            price       INTEGER NOT NULL,
            rating      REAL NOT NULL,
            nameni      TEXT NOT NULL,
            description TEXT
        )
    """)
    if c.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO products (name,category,brand,price,rating,nameni,description) VALUES (?,?,?,?,?,?,?)",
            SEED
        )
    conn.commit()
    conn.close()


def db_all():
    """Ги враќа сите производи сортирани по категорија и назив."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM products ORDER BY category, name").fetchall()
    conn.close()
    return rows


def db_add(name, category, brand, price, rating, nameni, description):
    """Додава нов производ во базата."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO products (name,category,brand,price,rating,nameni,description) VALUES (?,?,?,?,?,?,?)",
        (name, category, brand, price, rating, nameni, description)
    )
    conn.commit()
    conn.close()


def db_delete(pid):
    """Го брише производот со даденото ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()


def db_stats():
    """Враќа статистички податоци: вкупно, просечна цена, просечен рејтинг, по категорија, топ 3."""
    conn = sqlite3.connect(DB_PATH)
    total   = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    avg_p   = conn.execute("SELECT AVG(price) FROM products").fetchone()[0] or 0
    avg_r   = conn.execute("SELECT AVG(rating) FROM products").fetchone()[0] or 0
    cats    = conn.execute("SELECT category, COUNT(*) FROM products GROUP BY category").fetchall()
    top3    = conn.execute("SELECT name, rating FROM products ORDER BY rating DESC LIMIT 3").fetchall()
    conn.close()
    return {"total": total, "avg_price": avg_p, "avg_rating": avg_r, "categories": cats, "top3": top3}
