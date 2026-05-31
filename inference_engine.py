"""
inference_engine.py
Инференциски мотор — правила за филтрирање и препорака на производи.

Правила:
  1. Категоријата мора да се совпаѓа (или "Сите")
  2. Цената мора да биде <= максималниот буџет
  3. Намената мора да се совпаѓа (или "Сите")
  4. Рејтингот мора да биде >= минималниот рејтинг

Резултатот се сортира по рејтинг (опаѓачки), потоа по цена (растечки).
"""

import sqlite3
from database import DB_PATH


def preporacaj(category="Сите", namena="Сите", max_price=999999, min_rating=0.0):
    """
    Го применува инференцискиот мотор врз базата на знаење.

    Влез:
        category  (str)   — категорија на производ или "Сите"
        namena    (str)   — намена за употреба или "Сите"
        max_price (int)   — максимален буџет во денари
        min_rating(float) — минимален прифатлив рејтинг (0.0 - 5.0)

    Излез:
        Листа на tuple (id, name, category, brand, price, rating, nameni, description)
        сортирани по rating DESC, price ASC
    """
    conn = sqlite3.connect(DB_PATH)

    # Базично правило: буџет + рејтинг (секогаш се применуваат)
    sql    = "SELECT * FROM products WHERE price <= ? AND rating >= ?"
    params = [max_price, min_rating]

    # Правило 1: филтрирање по категорија
    if category != "Сите":
        sql += " AND category = ?"
        params.append(category)

    # Правило 2: филтрирање по намена (LIKE за частична совпаѓање)
    if namena != "Сите":
        sql += " AND nameni LIKE ?"
        params.append(f"%{namena}%")

    # Сортирање: прво по рејтинг (опаѓачки), потоа по цена (растечки)
    sql += " ORDER BY rating DESC, price ASC"

    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows
