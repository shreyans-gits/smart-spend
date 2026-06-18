import os
import sqlite3

DB_NAME = "expense_tracker.db"



def init_db(db_path: str = DB_NAME):
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                source TEXT NOT NULL,
                raw_text TEXT
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                date TEXT PRIMARY KEY,
                leftover REAL NOT NULL
            );
        """)

        cursor.execute("SELECT COUNT(*) FROM settings;")
        if cursor.fetchone()[0] == 0:
            default_settings = [
                ("daily_budget", "250.00"),
                ("rollover_enabled", "false")
            ]
            cursor.executemany(
                "INSERT INTO settings (key, value) VALUES (?, ?);", 
                default_settings
            )
            print("Database initialized with default settings.")
        else:
            print("Database tables verified. Settings already exist.")

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred during database initialization: {e}")
        conn.rollback()
        raise e

    finally:
        conn.close()

if __name__ == "__main__":
    init_db()