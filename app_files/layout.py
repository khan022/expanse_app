from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from add_transaction import AddTransactionScreen 

class MainLayout(FloatLayout):
    def __init__(self, app, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        # Store app reference in instance variable
        self.app = app

        # Ensure full window size
        Window.size = (600, 800)  # Adjust to match your screen size

        # Set up background image, stretching to cover the full layout
        with self.canvas.before:
            self.bg_image = Image(source='../Expense app/possible_bg2.jpg', allow_stretch=True, keep_ratio=False)
            self.add_widget(self.bg_image)

        # Top Buttons Layout (inside a BoxLayout)
        self.top_layout = BoxLayout(size_hint=(1, 0.2), pos_hint={'top': 1}, spacing=10, padding=20)

        # Top buttons with 80% height
        self.view_transactions_btn = Button(text='View all transactions', font_size=25, font_name="../fonts/EBGaramond-ExtraBold.ttf", size_hint_y=0.8, bold=True, background_color=[0, 0, 0, 0.6], padding=10)
        self.view_transactions_btn.bind(on_press=self.view_transactions)
        self.top_layout.add_widget(self.view_transactions_btn)

        self.add_transactions_btn = Button(text='Add Transactions', font_size=25, font_name="../fonts/EBGaramond-ExtraBold.ttf", size_hint_y=0.8, bold=True, background_color=[0, 0, 0, 0.6], padding=10)
        self.add_transactions_btn.bind(on_press=self.add_transactions)
        self.top_layout.add_widget(self.add_transactions_btn)

        self.add_widget(self.top_layout)

        # Create a BoxLayout for header + scrollable content
        layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), pos_hint={'y': 0}, padding=50)

        # Create the header row (not inside the ScrollView)
        header_layout = GridLayout(cols=2, size_hint_y=None, height=50, padding=[10, 10], spacing=10)

        # Header labels with fixed size
        header_place = Label(text='Place', bold=True, font_size=30, font_name = '../fonts/DancingScript-Regular.ttf', size_hint_y=None, height=50, color=[1, 1, 1, 1])
        header_balance = Label(text='Balance', bold=True, font_size=30, font_name = '../fonts/DancingScript-Regular.ttf', size_hint_y=None, height=50, color=[1, 1, 1, 1])

        # Add background for header
        self.add_background(header_place)
        self.add_background(header_balance)

        header_layout.add_widget(header_place)
        header_layout.add_widget(header_balance)

        layout.add_widget(header_layout)

        # Add a spacer (Widget) to create a gap between the headers and the data rows
        spacer = Widget(size_hint_y=None, height=10)  # Adjust the height to control the gap size
        layout.add_widget(spacer)

        # ScrollView for the balance table with an overlay effect
        scroll_view = ScrollView(size_hint=(1, 0.9))
        grid_layout = GridLayout(cols=2, size_hint_y=None, padding=[10, 10], spacing=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Fetch balance data from the database and display
        balances = self.app.get_balances()
        if balances:
            for balance_data in balances:
                place = balance_data[0]  
                balance = balance_data[1]  

                if place == 'Total':
                    place_label = Label(text=place, font_size=30, font_name ='../fonts/EBGaramond-Italic-VariableFont_wght.ttf', size_hint_y=None, height=50, color=[1, 1, 1, 1])
                    balance_label = Label(text=str(balance), font_size=28, font_name ='../fonts/EBGaramond-Italic-VariableFont_wght.ttf', size_hint_y=None, height=50, color=[1, 1, 1, 1])

                else:
                    place_label = Label(text=place, font_size=28, font_name ='../fonts/Cambo-Regular.ttf', size_hint_y=None, height=50, color=[1, 1, 1, 1])
                    balance_label = Label(text=str(balance), font_size=28, font_name ='../fonts/Cambo-Regular.ttf', size_hint_y=None, height=50, color=[1, 1, 1, 1])

                # Add background for each row
                self.add_background(place_label)
                self.add_background(balance_label)

                grid_layout.add_widget(place_label)
                grid_layout.add_widget(balance_label)

        scroll_view.add_widget(grid_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

    def add_background(self, widget):
        """ Add a semi-transparent background to the widget. """
        with widget.canvas.before:
            Color(0, 0, 0, 0.865)  # Black background with 60% opacity
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def view_transactions(self, instance):
        self.app.screen_manager.current = 'transactions'

    def add_transactions(self, instance):
        add_transaction_screen = AddTransactionScreen(app=self.app)  
        self.app.screen_manager.add_widget(add_transaction_screen)
        self.app.screen_manager.current = 'add_transaction' 