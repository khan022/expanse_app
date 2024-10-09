from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.modalview import ModalView
from kivy.graphics import Color, Rectangle
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
    balance = StringProperty('')
    reason = StringProperty('')

    def __init__(self, app, **kwargs):
        super(AddTransactionLayout, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'

        # Set the background image
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Set background color
            self.bg_image = Rectangle(source='../Expense app/possible_bg2.jpg', pos=self.pos, size=self.size)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widgets()

    def _update_rect(self, *args):
        self.bg_image.pos = self.pos
        self.bg_image.size = self.size

    def add_widgets(self):
        layout_container = BoxLayout(
            orientation='vertical',
            padding=[35, 80, 35, 80],
            size_hint=(0.8, 0.9), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        grid = GridLayout(cols=2, padding=10, spacing=10)
        grid.bind(minimum_height=grid.setter('height'))

        fields = [
            ("Date", self.create_date_widget()),
            ("Person", self.create_text_input_widget()),
            ("Place", self.create_place_spinner()),
            ("Amount", self.create_text_input_widget()),
            ("Balance", self.create_balance_spinner()),
            ("Reason", self.create_reason_input())
        ]

        for field_name, widget in fields:
            label = Label(
                text=f'{field_name}:',
                font_size=20,
                font_name='../fonts/Cambo-Regular.ttf',
                size_hint_y=None,
                height=40,  
                color=[1, 1, 1, 1]  
            )
            
            self.add_background(label)
            self.add_background(widget)

            grid.add_widget(label)
            grid.add_widget(widget)

        submit_button = Button(text='Add Transaction',font_size=20,
                                font_name='../fonts/Cambo-Regular.ttf', 
                                size_hint=(1, 0.1))
        submit_button.bind(on_press=self.add_transaction)


        grid.padding = [20, 20, 20, 80]

        layout_container.add_widget(grid)
        layout_container.add_widget(submit_button)
        self.add_widget(layout_container)

    def add_background(self, widget):
        with widget.canvas.before:
            Color(0, 0, 0, 0.8)
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(size=self.update, pos=self.update)

    def update(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def create_text_input_widget(self):
        self.person_input = TextInput(
            multiline=False,
            background_normal='',  # Remove default background
            background_color=(1, 1, 1, 0),  # White background with transparency
            foreground_color=(0, 0, 0, 1),  # Black text color
            halign='center',
            padding_y=(10, 10),
            size_hint_y=None,
            height=40,
            font_name='../fonts/Cambo-Regular.ttf',
        )
        return self.person_input

    def create_reason_input(self):
        self.reason_input = TextInput(
            multiline=True,
            background_normal='',  # Remove default background
            background_color=(1, 1, 1, .8),  # White background with transparency
            foreground_color=(1, 1, 1, 1),  # Black text color
            halign='center',
            padding_y=(10, 10),
            size_hint_y=None,
            height=80,  # Slightly taller for multiline input
            font_name='../fonts/Cambo-Regular.ttf',
        )
        return self.reason_input

    def create_date_widget(self):
        self.date_button = Button(text="Select Date", font_size=20,
                font_name='../fonts/Cambo-Regular.ttf', on_press=self.show_date_picker, 
                size_hint_y=None, height=40, background_normal='',  
                background_color=(1, 1, 1, 0.75),  
                color=(0, 0, 0, 1))
        return self.date_button

    def create_place_spinner(self):
        self.place_spinner = Spinner(
            text="Select Place",
            font_size=20,
            font_name='../fonts/Cambo-Regular.ttf',
            values=get_unique_places() + ["Add New Place"],
            size_hint=(1, None),
            height=40,
            background_normal='',  
            background_color=(1, 1, 1, 0.75),  
            color=(0, 0, 0, 1)
        )
        self.place_spinner.bind(text=self.on_place_selected)
        return self.place_spinner

    def create_balance_spinner(self):
        self.balance_spinner = Spinner(
            text='Select Balance',
            font_size=20,
            font_name='../fonts/Cambo-Regular.ttf',
            values=[str(bal[1]) for bal in get_all_balances()],  
            size_hint=(1, None),
            height=40,
            background_normal='',  
            background_color=(1, 1, 1, 0.75), 
            color=(0, 0, 0, 1)  
        )
        return self.balance_spinner

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
            self.update_balance_display(text)

    def update_balance_display(self, selected_place):
        balances = get_all_balances()
        for place, balance in balances:
            if place == selected_place:
                self.balance_spinner.text = str(balance)
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
            self.app.add_expense(self.date, self.person, self.place, float(self.amount), float(self.amount) + float(self.balance), self.reason)
            self.show_popup("Success", "Transaction added successfully!")
            self.clear_inputs()
        except Exception as e:
            self.show_popup("Error", f"Failed to add transaction: {e}")

    def validate_inputs(self):
        if not self.date or not self.person or not self.place or not self.amount or not self.balance or not self.reason:
            self.show_popup("Error", "All fields must be filled.")
            return False
        try:
            float(self.amount)  
            float(self.balance) 
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
        self.size_hint = (0.5, 0.5)
        self.callback = callback

        self.content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        today = datetime.today()
        self.selected_date = today

        self.year_input = TextInput(text=str(today.year), multiline=False, halign="center", font_size=24, size_hint_y=None, height=40)
        self.content.add_widget(Label(text="Year"))
        self.content.add_widget(self.year_input)

        self.month_input = TextInput(text=str(today.month), multiline=False, halign="center", font_size=24, size_hint_y=None, height=40)
        self.content.add_widget(Label(text="Month"))
        self.content.add_widget(self.month_input)

        self.day_input = TextInput(text=str(today.day), multiline=False, halign="center", font_size=24, size_hint_y=None, height=40)
        self.content.add_widget(Label(text="Day"))
        self.content.add_widget(self.day_input)

        submit_button = Button(text="Set Date", on_press=self.set_date, size_hint_y=None, height=40)
        self.content.add_widget(submit_button)

    def set_date(self, instance):
        try:
            year = int(self.year_input.text)
            month = int(self.month_input.text)
            day = int(self.day_input.text)

            selected_date = datetime(year, month, day)
            self.callback(selected_date)
            self.dismiss()
        except ValueError:
            error_popup = Popup(
                title="Invalid Date",
                content=Label(text="Please enter a valid date."),
                size_hint=(0.6, 0.4)
            )
            error_popup.open()
