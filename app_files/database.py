import sqlite3
import os

DATABASE_FILE = '../config/expenses.db'

def create_db():
    """ Create the database and expenses table if it doesn't exist. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            person TEXT NOT NULL,
            place TEXT NOT NULL,
            amount REAL NOT NULL,
            balance REAL NOT NULL,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(date, person, place, amount, balance, reason=None):
    """ Add a new expense to the database. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, person, place, amount, balance, reason)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, person, place, amount, balance, reason))
    conn.commit()
    conn.close()

def get_all_balances():
    """ Retrieve all current balances from the expenses table. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT place, SUM(balance) AS total_balance
        FROM expenses
        GROUP BY place
    ''')
    balances = cursor.fetchall()  # Returns list of tuples (place, total_balance)
    conn.close()
    return balances

def get_total_balance():
    """ Retrieve the total of all balances. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT SUM(balance) FROM expenses
    ''')
    total_balance = cursor.fetchone()[0]
    conn.close()
    return total_balance if total_balance else 0

def initialize_database():
    """ Initialize the database if it doesn't exist. """
    if not os.path.exists(DATABASE_FILE):
        create_db()


def get_last_ten_expenses():
    """ Retrieve the last 10 expenses from the database. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT date, person, place, amount, reason
        FROM expenses
        ORDER BY id DESC
        LIMIT 10
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows
