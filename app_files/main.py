from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from database import initialize_database, add_expense, get_all_balances, get_total_balance, get_last_ten_expenses
from layout import MainLayout
from view_transactions import ViewTransactionsLayout

class ExpenseApp(App):
    def build(self):
        # Initialize the database
        initialize_database()

        # Set up the ScreenManager to manage screens
        self.screen_manager = ScreenManager()

        # Add Main Layout
        self.main_layout = MainLayout(app=self)
        main_screen = Screen(name='main')
        main_screen.add_widget(self.main_layout)
        self.screen_manager.add_widget(main_screen)

        # Add View Transactions Layout
        self.view_transactions_layout = ViewTransactionsLayout(app=self)
        transactions_screen = Screen(name='transactions')
        transactions_screen.add_widget(self.view_transactions_layout)
        self.screen_manager.add_widget(transactions_screen)

        return self.screen_manager

    def add_expense(self, date, person, place, amount, balance, reason):
        """ Add an expense to the database. """
        try:
            add_expense(date, person, place, amount, balance, reason)
            print("Expense added successfully.")
        except Exception as e:
            print(f"Failed to add expense: {e}")

    def get_balances(self):
        """ Retrieve current balances from the database. """
        return get_all_balances()

    def get_total_balance(self):
        """ Retrieve the total balance from the database. """
        return get_total_balance()

    def get_last_ten_expenses(self):
        """ Retrieve the last ten expenses from the database. """
        return get_last_ten_expenses()

if __name__ == '__main__':
    ExpenseApp().run()
