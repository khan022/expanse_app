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

        self.app = app

        Window.size = (600, 800)

        with self.canvas.before:
            self.bg_image = Image(source='../Expense app/possible_bg2.jpg', allow_stretch=True, keep_ratio=False)
            self.add_widget(self.bg_image)

        self.top_layout = BoxLayout(size_hint=(1, 0.2), pos_hint={'top': 1}, spacing=10, padding=20)

        self.view_transactions_btn = Button(text='View all transactions', font_size=25, 
                                            font_name="../fonts/EBGaramond-ExtraBold.ttf", 
                                            size_hint_y=0.8, bold=True, background_color=[0, 0, 0, 0.6], 
                                            padding=10)
        self.view_transactions_btn.bind(on_press=self.view_transactions)
        self.top_layout.add_widget(self.view_transactions_btn)

        self.add_transactions_btn = Button(text='Add Transactions', font_size=25, 
                                           font_name="../fonts/EBGaramond-ExtraBold.ttf", 
                                           size_hint_y=0.8, bold=True, background_color=[0, 0, 0, 0.6], 
                                           padding=10)
        self.add_transactions_btn.bind(on_press=self.add_transactions)
        self.top_layout.add_widget(self.add_transactions_btn)

        self.add_widget(self.top_layout)

        layout = BoxLayout(orientation='vertical', size_hint=(1, 0.8), pos_hint={'y': 0}, padding=50)

        header_layout = GridLayout(cols=2, size_hint_y=None, height=50, padding=[10, 10], spacing=10)

        header_place = Label(text='Place', bold=True, font_size=30, 
                            font_name = '../fonts/DancingScript-Regular.ttf', 
                            size_hint_y=None, height=50, color=[1, 1, 1, 1])
        header_balance = Label(text='Balance', bold=True, font_size=30, 
                               font_name = '../fonts/DancingScript-Regular.ttf', 
                               size_hint_y=None, height=50, color=[1, 1, 1, 1])

        self.add_background(header_place)
        self.add_background(header_balance)

        header_layout.add_widget(header_place)
        header_layout.add_widget(header_balance)

        layout.add_widget(header_layout)

        spacer = Widget(size_hint_y=None, height=10)
        layout.add_widget(spacer)

        scroll_view = ScrollView(size_hint=(1, 0.9))
        grid_layout = GridLayout(cols=2, size_hint_y=None, padding=[10, 10], spacing=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        balances = self.app.get_balances()
        if balances:
            for balance_data in balances:
                place = balance_data[0]  
                balance = balance_data[1]  

                if place == 'Total':
                    place_label = Label(text=place, font_size=30, 
                                        font_name ='../fonts/EBGaramond-Italic-VariableFont_wght.ttf', 
                                        size_hint_y=None, height=50, color=[1, 1, 1, 1])
                    balance_label = Label(text=str(balance), font_size=28, 
                                        font_name ='../fonts/EBGaramond-Italic-VariableFont_wght.ttf', 
                                        size_hint_y=None, height=50, color=[1, 1, 1, 1])

                else:
                    place_label = Label(text=place, font_size=28, 
                                        font_name ='../fonts/Cambo-Regular.ttf', 
                                        size_hint_y=None, height=50, color=[1, 1, 1, 1])
                    balance_label = Label(text=str(balance), font_size=28, 
                                        font_name ='../fonts/Cambo-Regular.ttf', 
                                        size_hint_y=None, height=50, color=[1, 1, 1, 1])

                self.add_background(place_label)
                self.add_background(balance_label)

                grid_layout.add_widget(place_label)
                grid_layout.add_widget(balance_label)

        scroll_view.add_widget(grid_layout)
        layout.add_widget(scroll_view)

        self.add_widget(layout)

        # Logout button at the bottom center
        logout_button = Button(
                            text='Logout',
                            size_hint=(0.3, 0.05), 
                            pos_hint={'center_x': 0.5, 'y': 0},
                            background_normal='',  # Ensures no default background is used
                            background_color=(0.7, 0, 0, 0.8),  # Semi-transparent black (R, G, B, alpha)
                            color=(1, 1, 1, 1)  # White text color (R, G, B, alpha)
                        )
        logout_button.bind(on_press=self.logout)
        self.add_widget(logout_button)

    def add_background(self, widget):
        """ Add a semi-transparent background to the widget. """
        with widget.canvas.before:
            Color(0, 0, 0, 0.865) 
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

    def logout(self, instance):
        self.app.root.current = 'login'  # Navigate back to the login screen
