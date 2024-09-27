from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainLayout(BoxLayout):
    def __init__(self, app, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'

        # Input fields
        self.date_input = TextInput(hint_text='Date (MM/DD/YYYY)', multiline=False)
        self.person_input = TextInput(hint_text='Person', multiline=False)
        self.place_input = TextInput(hint_text='Place', multiline=False)
        self.amount_input = TextInput(hint_text='Amount', multiline=False)
        self.balance_input = TextInput(hint_text='Balance', multiline=False)
        self.reason_input = TextInput(hint_text='Reason', multiline=False)

        self.add_widget(self.date_input)
        self.add_widget(self.person_input)
        self.add_widget(self.place_input)
        self.add_widget(self.amount_input)
        self.add_widget(self.balance_input)
        self.add_widget(self.reason_input)

        # Buttons
        self.add_button = Button(text='Add Expense')
        self.show_balances_button = Button(text='Show Balances')
        
        self.add_button.bind(on_press=self.add_expense)
        self.show_balances_button.bind(on_press=self.show_balances)

        self.add_widget(self.add_button)
        self.add_widget(self.show_balances_button)

        # Balance label
        self.balance_label = Label(text='Balances will be shown here')
        self.add_widget(self.balance_label)

    def add_expense(self, instance):
        """ Add expense to the database and handle UI update. """
        date = self.date_input.text
        person = self.person_input.text
        place = self.place_input.text
        amount = float(self.amount_input.text)
        balance = float(self.balance_input.text)
        reason = self.reason_input.text

        self.app.add_expense(date, person, place, amount, balance, reason)

        # Clear input fields after adding
        self.date_input.text = ''
        self.person_input.text = ''
        self.place_input.text = ''
        self.amount_input.text = ''
        self.balance_input.text = ''
        self.reason_input.text = ''

    def show_balances(self, *args):  # Accept additional arguments
        """ Show current balances in the text area. """
        balances = self.app.get_balances()
        balance_text = "Place\tBalance\n"  # Header for the balance display
        balance_text += "\n".join([f"{place}\t{total_balance}" for (place, total_balance) in balances])
        self.balance_label.text = balance_text
