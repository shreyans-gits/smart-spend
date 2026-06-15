import sqlite3
from datetime import datetime, timedelta
from db.schema import DB_NAME
from models.expense import Expense
import config
from models.expense import Expense

def get_yesterday_leftover(today_date: str, db_path: str = DB_NAME) -> float:
    try:
        today_dt = datetime.strptime(today_date, "%Y-%m-%d")
        yesterday_dt = today_dt - timedelta(days=1)
        yesterday_date = yesterday_dt.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid today_date format '{today_date}'. Expected 'YYYY-MM-DD'.")

    query = "SELECT leftover FROM daily_summary WHERE date = ?;"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (yesterday_date,))
        result = cursor.fetchone()
        return float(result[0]) if result is not None else 0.0
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error during get_yesterday_leftover: {e}") from e
    finally:
        conn.close()


def save_daily_summary(date: str, leftover: float, db_path: str = DB_NAME):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid summary date format '{date}'. Expected 'YYYY-MM-DD'.")

    query = """
        INSERT INTO daily_summary (date, leftover)
        VALUES (?, ?)
        ON CONFLICT(date) DO UPDATE SET leftover = excluded.leftover;
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (date, leftover))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Database error during save_daily_summary: {e}") from e
    finally:
        conn.close()

def validate_expense_data(date_str: str, source: str, category: str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format '{date_str}'. Expected 'YYYY-MM-DD'.")

    if source not in ("scan", "manual"):
        raise ValueError(f"Invalid source '{source}'. Must be either 'scan' or 'manual'.")

    if category not in config.VALID_CATEGORIES:
        raise ValueError(f"Invalid category '{category}'. Must be one of {config.VALID_CATEGORIES}.")


def add_expense(date: str, amount: float, category: str, source: str, raw_text: str = None, db_path: str = DB_NAME) -> int:
    validate_expense_data(date_str=date, source=source, category=category)

    query = """
        INSERT INTO expenses (date, amount, category, source, raw_text)
        VALUES (?, ?, ?, ?, ?);
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (date, amount, category, source, raw_text))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Database error during add_expense: {e}") from e
    finally:
        conn.close()


def get_expenses_by_date(date: str, db_path: str = DB_NAME) -> list:
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid query date format '{date}'. Expected 'YYYY-MM-DD'.")

    query = """
        SELECT id, date, amount, category, source, raw_text 
        FROM expenses 
        WHERE date = ?;
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (date,))
        rows = cursor.fetchall()
        return [Expense(*row) for row in rows]
    
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error during get_expenses_by_date: {e}") from e
    
    finally:
        conn.close()


def get_daily_total(date: str, db_path: str = DB_NAME) -> float:
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid total date format '{date}'. Expected 'YYYY-MM-DD'.")

    query = "SELECT SUM(amount) FROM expenses WHERE date = ?;"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (date,))
        result = cursor.fetchone()[0]
        return float(result) if result is not None else 0.0
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error during get_daily_total: {e}") from e
    finally:
        conn.close()


def get_settings(db_path: str = DB_NAME) -> dict:
    query = "SELECT key, value FROM settings;"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return {row[0]: row[1] for row in rows}
    except sqlite3.Error as e:
        raise sqlite3.Error(f"Database error during get_settings: {e}") from e
    finally:
        conn.close()


def update_settings(key: str, value: str, db_path: str = DB_NAME):
    query = """
        INSERT INTO settings (key, value) 
        VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value;
    """
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute(query, (key, value))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise sqlite3.Error(f"Database error during update_settings: {e}") from e
    finally:
        conn.close()