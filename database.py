import sqlite3
import os

DATABASE_FILE = 'expenses.db'

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

def get_all_balances(conn):
    """ Retrieve all current balances from the expenses table. """
    cursor = conn.cursor()
    cursor.execute('''
        SELECT place, SUM(balance) AS total_balance
        FROM expenses
        GROUP BY place
    ''')
    return cursor.fetchall()  # Returns list of tuples (place, total_balance)

def initialize_database():
    """ Initialize the database if it doesn't exist. """
    if not os.path.exists(DATABASE_FILE):
        create_db()
