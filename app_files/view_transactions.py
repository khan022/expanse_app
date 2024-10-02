from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

class ViewTransactionsLayout(FloatLayout):
    def __init__(self, app, **kwargs):
        super(ViewTransactionsLayout, self).__init__(**kwargs)
        self.app = app

        # Add background image
        with self.canvas.before:
            self.bg_image = Image(source='../Expense app/possible_bg2.jpg', allow_stretch=True, keep_ratio=False)
            self.add_widget(self.bg_image)

        # Create a ScrollView to display transactions
        scroll_view = ScrollView(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        grid_layout = GridLayout(cols=4, size_hint_y=None, padding=[10, 10], spacing=10)  # Updated to 4 columns
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Fetch last 10 expenses
        last_ten_expenses = self.app.get_last_ten_expenses()

        # Create headers with background color
        date_header = Label(text='Date', bold=True, size_hint_y=None, height=40, color=[1, 1, 1, 1])
        place_header = Label(text='Place', bold=True, size_hint_y=None, height=40, color=[1, 1, 1, 1])
        amount_header = Label(text='Amount', bold=True, size_hint_y=None, height=40, color=[1, 1, 1, 1])
        reason_header = Label(text='Reason', bold=True, size_hint_y=None, height=40, color=[1, 1, 1, 1])

        # Add background for headers
        self.add_background(date_header)
        self.add_background(place_header)
        self.add_background(amount_header)
        self.add_background(reason_header)

        grid_layout.add_widget(date_header)
        grid_layout.add_widget(place_header)
        grid_layout.add_widget(amount_header)
        grid_layout.add_widget(reason_header)

        if last_ten_expenses:
            for expense in last_ten_expenses:
                # Assuming 'date', 'place', 'amount', and 'reason' are at indices 0, 2, 4, and 5 respectively
                date_label = Label(text=expense[0], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # Date
                place_label = Label(text=expense[2], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # Place
                amount_label = Label(text=str(expense[4]), size_hint_y=None, height=40, color=[1, 1, 1, 1])  # Amount
                reason_label = Label(text=expense[5], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # Reason

                # Add background for each row
                self.add_background(date_label)
                self.add_background(place_label)
                self.add_background(amount_label)
                self.add_background(reason_label)

                grid_layout.add_widget(date_label)
                grid_layout.add_widget(place_label)
                grid_layout.add_widget(amount_label)
                grid_layout.add_widget(reason_label)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

        # Back button to return to the main screen
        back_button = Button(text='Back', size_hint=(0.1, 0.1), pos_hint={'right': 1, 'top': 1}, background_color=[0, 0, 0, 0.6])
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def add_background(self, widget):
        """ Add a semi-transparent background to the widget. """
        with widget.canvas.before:
            Color(0, 0, 0, 0.6)  # Black background with 60% opacity
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def go_back(self, instance):
        """ Go back to the main screen. """
        self.app.screen_manager.current = 'main'  # Navigate back to the main screen
