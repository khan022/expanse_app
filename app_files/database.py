import sqlite3
import os

DATABASE_FILE = '../config/expense.db'

def create_db():
    """ Create the database and expenses table if it doesn't exist. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            person TEXT NOT NULL,
            place TEXT NOT NULL,
            amount INTEGER NOT NULL,
            balance INTEGER NOT NULL,
            reason TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_expense(date, person, place, amount, balance, reason=None):
    """ Add a new expense to the database. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO expenses (date, person, place, amount, balance, reason)
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (date, person, place, amount, balance, reason))
    conn.commit()
    conn.close()

def get_all_balances():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT place, balance
                      FROM (
                          SELECT e.place, e.balance, e.id,
                                 ROW_NUMBER() OVER (PARTITION BY e.place ORDER BY e.id DESC) as rn
                          FROM expenses e
                      ) subquery
                      WHERE rn = 1''')

    balances = cursor.fetchall()
    total_balance = sum([balance for _, balance in balances])
    balances.append(('Total', total_balance))
    conn.close()
    return balances

def get_unique_places():
    """ Retrieve a list of unique places from the expenses table. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT place FROM expenses")
    places = [place[0] for place in cursor.fetchall()]  # Fetch unique places
    conn.close()
    return places

def get_last_balance_for_place(place):
    """ Get the last balance for a specific place. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT balance FROM expenses
                      WHERE place = ?
                      ORDER BY id DESC
                      LIMIT 1''', (place,))
    last_balance = cursor.fetchone()
    conn.close()
    return last_balance[0] if last_balance else 0  # Return balance or 0 if no entry found

def get_total_balance():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(balance) FROM expenses''')
    total_balance = cursor.fetchone()[0]
    conn.close()
    return total_balance if total_balance else 0

def initialize_database():
    if not os.path.exists(DATABASE_FILE):
        create_db()

def get_last_ten_expenses():
    conn = sqlite3.connect(DATABASE_FILE) 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC LIMIT 10")
    
    expenses = cursor.fetchall()
    conn.close()
    
    return expenses


def get_last_balance_for_place(place):
    """ Retrieve the last balance for a specific place. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT balance
        FROM expenses
        WHERE place = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (place,))
    last_balance = cursor.fetchone()
    conn.close()
    
    return last_balance[0] if last_balance else 0 

def add_new_place(place):
    """ Add a new place to the database. """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (place, balance) VALUES (?, ?)
    ''', (place, 0))  # You can set a default balance, if needed
    conn.commit()
    conn.close()

