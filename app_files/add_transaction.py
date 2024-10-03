from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from datetime import datetime
from database import get_all_balances, get_unique_places, add_expense

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
    balance = StringProperty('')  # Balance is now StringProperty
    reason = StringProperty('')

    def __init__(self, app, **kwargs):
        super(AddTransactionLayout, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'
        self.add_widgets()

    def add_widgets(self):
        grid = GridLayout(cols=2, padding=10, spacing=10)

        grid.add_widget(Label(text='Date:'))
        self.date_button = Button(text="Select Date", on_press=self.show_date_picker)
        grid.add_widget(self.date_button)

        grid.add_widget(Label(text='Person:'))
        self.person_input = TextInput(multiline=False)
        grid.add_widget(self.person_input)

        grid.add_widget(Label(text='Place:'))
        self.place_spinner = Spinner(
            text="Select Place",
            values=get_unique_places() + ["Add New Place"],
            size_hint=(1, None)
        )
        self.place_spinner.bind(text=self.on_place_selected)
        grid.add_widget(self.place_spinner)

        grid.add_widget(Label(text='Amount:'))
        self.amount_input = TextInput(multiline=False)
        grid.add_widget(self.amount_input)

        grid.add_widget(Label(text='Balance:'))
        self.balance_spinner = Spinner(
            text='Select Balance',
            values=[str(bal[1]) for bal in get_all_balances()]  # Get balances as strings
        )
        grid.add_widget(self.balance_spinner)

        grid.add_widget(Label(text='Reason:'))
        self.reason_input = TextInput(multiline=True)
        grid.add_widget(self.reason_input)

        submit_button = Button(text='Add Transaction', size_hint=(1, 0.2))
        submit_button.bind(on_press=self.add_transaction)
        self.add_widget(grid)
        self.add_widget(submit_button)

    def show_date_picker(self, instance):
        date_popup = DatePicker(callback=self.on_date_selected)
        date_popup.open()

    def on_date_selected(self, date_obj):
        self.date_button.text = date_obj.strftime('%Y-%m-%d')
        self.date = date_obj.strftime('%Y-%m-%d')

    def on_place_selected(self, spinner, text):
        if text == "Add New Place":
            self.show_new_place_popup()
        else:
            # Update balance when a place is selected
            self.update_balance_display(text)

    def update_balance_display(self, selected_place):
        balances = get_all_balances()
        for place, balance in balances:
            if place == selected_place:
                self.balance_spinner.text = str(balance)  # Update the balance display
                break

    def show_new_place_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text="Enter New Place:")
        new_place_input = TextInput(multiline=False)
        submit_button = Button(text="Add Place", size_hint=(1, 0.2))

        content.add_widget(label)
        content.add_widget(new_place_input)
        content.add_widget(submit_button)

        popup = ModalView(size_hint=(0.75, 0.4))
        popup.add_widget(content)

        def add_place(instance):
            new_place = new_place_input.text.strip()
            if new_place:
                self.place_spinner.values = list(self.place_spinner.values) + [new_place]
                self.place_spinner.text = new_place
            popup.dismiss()

        submit_button.bind(on_press=add_place)
        popup.open()

    def add_transaction(self, instance):
        self.person = self.person_input.text.strip()
        self.place = self.place_spinner.text.strip()
        self.amount = self.amount_input.text.strip()
        self.balance = self.balance_spinner.text.strip()
        self.reason = self.reason_input.text.strip()

        if not self.validate_inputs():
            return

        try:
            self.app.add_expense(self.date, self.person, self.place, float(self.amount), float(self.balance), self.reason)
            self.show_popup("Success", "Transaction added successfully!")
            self.clear_inputs()
        except Exception as e:
            self.show_popup("Error", f"Failed to add transaction: {e}")

    def validate_inputs(self):
        if not self.date or not self.person or not self.place or not self.amount or not self.balance or not self.reason:
            self.show_popup("Error", "All fields must be filled.")
            return False
        try:
            float(self.amount)  # Check if amount is a valid float
            float(self.balance)  # Check if balance is a valid float
        except ValueError:
            self.show_popup("Error", "Amount and Balance must be numbers.")
            return False
        return True

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()

    def clear_inputs(self):
        self.date_button.text = "Select Date"
        self.person_input.text = ''
        self.place_spinner.text = 'Select Place'
        self.amount_input.text = ''
        self.balance_spinner.text = 'Select Balance'
        self.reason_input.text = ''

class DatePicker(Popup):
    def __init__(self, callback, **kwargs):
        super(DatePicker, self).__init__(**kwargs)
        self.title = "Select Date"
        self.size_hint = (0.8, 0.8)
        self.callback = callback

        self.content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        today = datetime.today()
        self.selected_date = today

        self.year_input = TextInput(text=str(today.year), multiline=False, halign="center", font_size=24)
        self.content.add_widget(Label(text="Year"))
        self.content.add_widget(self.year_input)

        self.month_input = TextInput(text=str(today.month), multiline=False, halign="center", font_size=24)
        self.content.add_widget(Label(text="Month"))
        self.content.add_widget(self.month_input)

        self.day_input = TextInput(text=str(today.day), multiline=False, halign="center", font_size=24)
        self.content.add_widget(Label(text="Day"))
        self.content.add_widget(self.day_input)

        submit_button = Button(text="Set Date", on_press=self.set_date)
        self.content.add_widget(submit_button)

    def set_date(self, instance):
        try:
            year = int(self.year_input.text)
            month = int(self.month_input.text)
            day = int(self.day_input.text)

            selected_date = datetime(year, month, day)
            self.selected_date = selected_date
            self.callback(selected_date)
            self.dismiss()
        except ValueError:
            error_popup = Popup(
                title="Invalid Date",
                content=Label(text="Please enter a valid date."),
                size_hint=(0.6, 0.3)
            )
            error_popup.open()
