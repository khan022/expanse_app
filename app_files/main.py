from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from database import initialize_database, add_expense, get_all_balances, get_unique_places, get_total_balance, get_last_ten_expenses
from layout import MainLayout
from view_transactions import ViewTransactionsLayout
from add_transaction import AddTransactionScreen  # Import the AddTransactionScreen
from login import LoginScreen  # Import the LoginScreen

class ExpenseApp(App):
    def build(self):
        # Initialize the database
        initialize_database()

        # Set up the ScreenManager to manage screens
        self.screen_manager = ScreenManager()

        # Add Login Screen
        self.login_screen = LoginScreen(app=self)
        self.login_screen.name = 'login'  # Set the name for the LoginScreen
        self.screen_manager.add_widget(self.login_screen)

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

        # Add Add Transaction Screen
        self.add_transaction_screen = AddTransactionScreen(app=self)
        self.add_transaction_screen.name = "add_transaction"  # Set the screen name
        self.screen_manager.add_widget(self.add_transaction_screen)

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
    
    def get_unique_places(self):
        """ Retrieve the last ten expenses from the database. """
        return get_unique_places()
    
    def logout(self, instance):
        self.app.screen_manager.current = 'login'  # Use 'login' if that is the name of the LoginScreen


if __name__ == '__main__':
    ExpenseApp().run()
