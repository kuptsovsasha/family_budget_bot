import sqlite3
import os
from datetime import datetime
from config import logger, SQLITE_DB_FILE
from .models import INCOME_CATEGORIES, EXPENSE_CATEGORIES

# SQL statements optimized for SQLite
CREATE_CATEGORIES_TABLE_SQLITE = '''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('income', 'expense'))
)
'''

CREATE_TRANSACTIONS_TABLE_SQLITE = '''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
)
'''


def dict_factory(cursor, row):
    """Convert SQLite row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db_connection():
    """Create and return a connection to the SQLite database"""
    conn = sqlite3.connect(SQLITE_DB_FILE)
    conn.row_factory = dict_factory
    return conn


def setup_database():
    """
    Initialize the SQLite database and create required tables if they don't exist.
    Also populates default categories.
    """
    try:
        logger.info(f"Setting up SQLite database at {SQLITE_DB_FILE}...")

        # Create directory for database if it doesn't exist
        db_dir = os.path.dirname(SQLITE_DB_FILE)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

        conn = sqlite3.connect(SQLITE_DB_FILE)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(CREATE_CATEGORIES_TABLE_SQLITE)
        cursor.execute(CREATE_TRANSACTIONS_TABLE_SQLITE)

        # Check if categories table is empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]

        if count == 0:
            logger.info("Populating default categories in SQLite...")
            for category in INCOME_CATEGORIES:
                cursor.execute("INSERT INTO categories (name, type) VALUES (?, ?)",
                               (category, 'income'))

            for category in EXPENSE_CATEGORIES:
                cursor.execute("INSERT INTO categories (name, type) VALUES (?, ?)",
                               (category, 'expense'))

        conn.commit()
        logger.info("SQLite database setup completed successfully")

    except sqlite3.Error as err:
        logger.error(f"SQLite database setup failed: {err}")
        raise

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()


class DBHandler:
    """
    Handler for all database operations using SQLite.
    """

    @staticmethod
    def add_transaction(user_id, category_id, amount, description=None):
        """Add a new transaction to the database"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Format datetime as ISO string for SQLite
            date_str = datetime.now().isoformat()

            query = """
            INSERT INTO transactions (user_id, category_id, amount, description, date)
            VALUES (?, ?, ?, ?, ?)
            """

            cursor.execute(query, (user_id, category_id, amount, description, date_str))
            conn.commit()
            logger.info(f"Transaction added for user {user_id}, category {category_id}")

        except sqlite3.Error as err:
            logger.error(f"Error adding transaction: {err}")
            if conn:
                conn.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_category_info(category_id):
        """Get category information by ID"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "SELECT id, name, type FROM categories WHERE id = ?"
            cursor.execute(query, (category_id,))
            category = cursor.fetchone()

            return category

        except sqlite3.Error as err:
            logger.error(f"Error getting category info: {err}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_categories(transaction_type):
        """Get all categories of a specific type"""
        conn = None
        cursor = None
        try:
            conn = sqlite3.connect(SQLITE_DB_FILE)  # Don't use dict factory here
            cursor = conn.cursor()

            query = "SELECT id, name FROM categories WHERE type = ? ORDER BY name"
            cursor.execute(query, (transaction_type,))
            categories = cursor.fetchall()

            return categories

        except sqlite3.Error as err:
            logger.error(f"Error getting categories: {err}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_transactions(user_id, start_date, end_date):
        """Get all transactions in a date range for a user"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Format dates for SQLite
            start_str = start_date.isoformat()
            end_str = end_date.isoformat()

            query = """
            SELECT t.id, t.amount, t.description, t.date, c.name as category, c.type
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.user_id = ? AND t.date BETWEEN ? AND ?
            ORDER BY t.date DESC
            """

            cursor.execute(query, (user_id, start_str, end_str))
            transactions = cursor.fetchall()

            return transactions

        except sqlite3.Error as err:
            logger.error(f"Error getting transactions: {err}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    @staticmethod
    def get_category_summary(start_date, end_date):
        """Get a summary of transactions by category in a date range"""
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Format dates for SQLite
            start_str = start_date.isoformat()
            end_str = end_date.isoformat()

            query = """
            SELECT c.name as category, c.type, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.date BETWEEN ? AND ?
            GROUP BY c.id
            ORDER BY c.type, total DESC
            """

            cursor.execute(query, (start_str, end_str))
            summary = cursor.fetchall()

            return summary

        except sqlite3.Error as err:
            logger.error(f"Error getting category summary: {err}")
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
