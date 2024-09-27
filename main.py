from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from database import initialize_database, add_expense, get_all_balances
from layout import MainLayout
import sqlite3

class ExpenseApp(App):
    def build(self):
        # Initialize the database
        initialize_database()

        self.main_layout = MainLayout(app=self)
        return self.main_layout

    def add_expense(self, date, person, place, amount, balance, reason):
        """ Add expense to the database. """
        try:
            add_expense(date, person, place, amount, balance, reason)
            print("Expense added successfully.")
        except Exception as e:
            print(f"Failed to add expense: {e}")

    def get_balances(self):
        """ Retrieve current balances from the database. """
        conn = sqlite3.connect('expenses.db')
        balances = get_all_balances(conn)
        conn.close()
        return balances

if __name__ == '__main__':
    ExpenseApp().run()
