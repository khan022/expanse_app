from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from database import get_all_balances, get_unique_places, get_last_balance_for_place, add_new_place  # Ensure this function is defined in your database module


class AddTransactionScreen(Screen):
    def __init__(self, app, **kwargs):
        super(AddTransactionScreen, self).__init__(**kwargs)
        self.app = app
        self.layout = AddTransactionLayout(app)
        self.add_widget(self.layout)


class AddTransactionLayout(BoxLayout):
    date = StringProperty('')
    person = StringProperty('')
    place = StringProperty('')
    amount = StringProperty('')
    balance = StringProperty('')
    reason = StringProperty('')

    def __init__(self, app, **kwargs):
        super(AddTransactionLayout, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.add_widgets()

    def add_widgets(self):
        # Create a GridLayout for better organization
        grid = GridLayout(cols=2, padding=10, spacing=10)

        # Labels and Text Inputs
        grid.add_widget(Label(text='Date:'))
        self.date_input = TextInput(multiline=False)
        grid.add_widget(self.date_input)

        grid.add_widget(Label(text='Person:'))
        self.person_input = TextInput(multiline=False)
        grid.add_widget(self.person_input)

        grid.add_widget(Label(text='Place:'))

        # Place Spinner with last balance display
        self.place_spinner = Spinner(
            text='Select Place',
            values=get_unique_places(),  # Assuming you have a function to retrieve unique places
            size_hint=(1, None),  # Allow the spinner to stretch
            height=44  # Set a height for better visibility
        )
        self.place_spinner.bind(text=self.update_balance)  # Update balance when a place is selected
        grid.add_widget(self.place_spinner)

        # Button to add a new place
        self.new_place_input = TextInput(hint_text='Add New Place', multiline=False)
        grid.add_widget(self.new_place_input)

        add_place_button = Button(text='Add Place', size_hint=(1, None), height=44)
        add_place_button.bind(on_press=self.add_place)
        grid.add_widget(add_place_button)

        grid.add_widget(Label(text='Last Balance:'))
        self.balance_label = Label(text='')  # Label to display the last balance
        grid.add_widget(self.balance_label)

        grid.add_widget(Label(text='Amount:'))
        self.amount_input = TextInput(multiline=False)
        grid.add_widget(self.amount_input)

        grid.add_widget(Label(text='Reason:'))
        self.reason_input = TextInput(multiline=True)
        grid.add_widget(self.reason_input)

        # Submit Button
        submit_button = Button(text='Add Transaction', size_hint=(1, 0.2))
        submit_button.bind(on_press=self.add_transaction)
        self.add_widget(grid)
        self.add_widget(submit_button)

    def update_balance(self, spinner, text):
        """Update the balance label based on the selected place."""
        last_balance = get_last_balance_for_place(text)  # Fetch the last balance for the selected place
        self.balance_label.text = f'Last Balance: {last_balance}'

    def add_place(self, instance):
        """Add a new place to the database and update the spinner."""
        new_place = self.new_place_input.text.strip()
        if new_place:
            add_new_place(new_place)  # Function to add the new place to the database
            self.place_spinner.values = get_unique_places()  # Refresh the spinner values
            self.new_place_input.text = ''  # Clear the input
            self.show_popup("Success", "New place added successfully!")
        else:
            self.show_popup("Error", "Place name cannot be empty.")

    def add_transaction(self, instance):
        # Get values from inputs
        self.date = self.date_input.text.strip()
        self.person = self.person_input.text.strip()
        self.place = self.place_spinner.text.strip()
        self.amount = self.amount_input.text.strip()
        self.reason = self.reason_input.text.strip()

        # Validate input
        if not self.validate_inputs():
            return

        # Call the app's add_expense method
        try:
            self.app.add_expense(self.date, self.person, self.place, float(self.amount), self.balance_label.text.split(': ')[-1], self.reason)
            self.show_popup("Success", "Transaction added successfully!")
            self.clear_inputs()
        except Exception as e:
            self.show_popup("Error", f"Failed to add transaction: {e}")

    def validate_inputs(self):
        if not self.date or not self.person or not self.place or not self.amount or not self.reason:
            self.show_popup("Error", "All fields must be filled.")
            return False
        try:
            float(self.amount) 
        except ValueError:
            self.show_popup("Error", "Amount must be a number.")
            return False
        return True

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def clear_inputs(self):
        self.date_input.text = ''
        self.person_input.text = ''
        self.place_spinner.text = 'Select Place'
        self.amount_input.text = ''
        self.balance_label.text = '' 
        self.reason_input.text = ''
        self.new_place_input.text = '' 
