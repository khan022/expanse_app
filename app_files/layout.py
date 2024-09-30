from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from view_transactions import ViewTransactionsLayout  # Import the ViewTransactionsLayout class

class MainLayout(FloatLayout):
    def __init__(self, app, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.app = app

        # Ensure full window size
        Window.size = (600, 800)  # Adjust to match your screen size

        # Set up background image, stretching to cover the full layout
        with self.canvas.before:
            self.bg_image = Image(source='../Expense app/possible_bg1.jpg', allow_stretch=True, keep_ratio=False)
            self.add_widget(self.bg_image)

        # Top Buttons Layout (inside a BoxLayout)
        self.top_layout = BoxLayout(size_hint=(1, 0.2), pos_hint={'top': 1}, spacing=10)
        self.view_transactions_btn = Button(text='View all transactions', font_size=24, size_hint=(0.5, 1), bold=True, background_color=[0, 0, 0, 0.6])
        self.view_transactions_btn.bind(on_press=self.view_transactions)
        self.top_layout.add_widget(self.view_transactions_btn)

        self.add_transactions_btn = Button(text='Add Transactions', font_size=24, size_hint=(0.5, 1), bold=True, background_color=[0, 0, 0, 0.6])
        self.add_transactions_btn.bind(on_press=self.add_transactions)
        self.top_layout.add_widget(self.add_transactions_btn)

        self.add_widget(self.top_layout)

        # ScrollView for the balance table with an overlay effect
        grid_layout = GridLayout(cols=2, size_hint_y=None, padding=[10, 10], spacing=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Header (semi-transparent background for contrast)
        header_place = Label(text='Place', bold=True, font_size=32, size_hint_y=None, height=50, color=[1, 1, 1, 1])
        header_balance = Label(text='Balance', bold=True, font_size=32, size_hint_y=None, height=50, color=[1, 1, 1, 1])
        
        # Add background for header
        self.add_background(header_place)
        self.add_background(header_balance)
        
        grid_layout.add_widget(header_place)
        grid_layout.add_widget(header_balance)

        # Fetch balance data from the database and display
        balances = self.app.get_balances()
        scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={'y': 0})
        if balances:
            for balance_data in balances:
                place = balance_data[0]  # Assuming it's the place column
                balance = balance_data[1]  # Assuming it's the balance column

                place_label = Label(text=place, font_size=28, size_hint_y=None, height=50, color=[1, 1, 1, 1])
                balance_label = Label(text=str(balance), font_size=28, size_hint_y=None, height=50, color=[1, 1, 1, 1])

                # Add background for each row
                self.add_background(place_label)
                self.add_background(balance_label)

                grid_layout.add_widget(place_label)
                grid_layout.add_widget(balance_label)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

    def add_background(self, widget):
        """ Add a semi-transparent background to the widget. """
        with widget.canvas.before:
            Color(0, 0, 0, 0.6)  # Black background with 60% opacity
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def view_transactions(self, instance):
        """ Navigate to the ViewTransactionsLayout. """
        self.clear_widgets()  # Clear the current layout
        view_transactions_layout = ViewTransactionsLayout(self.app)  # Create an instance of ViewTransactionsLayout
        self.add_widget(view_transactions_layout)  # Add the new layout

    def add_transactions(self, instance):
        # Logic for adding a new transaction
        popup = Popup(title='Add Transaction',
                      content=Label(text='Add transaction form will be here...'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()
