"""
main.py
Влезна точка на апликацијата.
Стартување: python main.py
"""

from database import init_db
from gui import start_app

if __name__ == "__main__":
    init_db()      # Иницијализирај ја базата (се прескокнува ако веќе постои)
    start_app()    # Стартувај го GUI
