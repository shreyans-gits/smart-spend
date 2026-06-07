import sqlite3
from datetime import datetime
from db.schema import DB_NAME
from models.expense import Expense
from config import VALID_CATEGORIES


def validate_expense_data(date_str: str, source: str, category: str):
    """Helper validation to enforce strict schema constraints."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format '{date_str}'. Expected 'YYYY-MM-DD'.")

    if source not in ("scan", "manual"):
        raise ValueError(f"Invalid source '{source}'. Must be either 'scan' or 'manual'.")

    if category not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category '{category}'. Must be one of {VALID_CATEGORIES}.")


def add_expense(date: str, amount: float, category: str, source: str, raw_text: str = None, db_path: str = DB_NAME) -> int:
    """
    Validates and inserts a new expense into the database.
    Returns the auto-generated ID of the inserted row.
    """
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
    """
    Retrieves all expenses matching a specific YYYY-MM-DD date.
    
    TODO: Refactor to return a list of Expense dataclass instances 
          instead of raw tuples once models/expense.py is finished.
    """
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
    """
    Calculates the sum total of all expenses for a specific date.
    Returns 0.0 if there are no expenses.
    """
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
    """
    Retrieves all application settings as key-value pairs.
    Returns a flat dictionary (e.g., {'daily_budget': '50.00'}).
    """
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
    """
    Updates or inserts a configuration setting key-value pair.
    Values should be passed as strings to maintain database uniformity.
    """
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