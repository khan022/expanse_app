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

        # Set up background image, stretching to cover the full layout
        with self.canvas.before:
            self.bg_image = Image(source='../Expense app/possible_bg2.jpg', allow_stretch=True, keep_ratio=False)
            self.add_widget(self.bg_image)

        # Add some padding at the top of the layout
        top_padding = FloatLayout(size_hint=(1, 0.1))  # This will act as padding
        self.add_widget(top_padding)

        # Create a ScrollView to display transactions
        scroll_view = ScrollView(size_hint=(1, 0.8), pos_hint={'x': 0, 'y': 0})
        grid_layout = GridLayout(cols=5, size_hint_y=None, padding=[10, 10], spacing=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Fetch last 10 expenses
        last_ten_expenses = self.app.get_last_ten_expenses()
        print(last_ten_expenses)

        # Create headers
        headers = ['Date', 'Person', 'Place', 'Amount', 'Reason']
        for header in headers:
            header_label = Label(text=header, bold=True, size_hint_y=None, height=40, color=[1, 1, 1, 1])
            self.add_background(header_label)
            grid_layout.add_widget(header_label)

        # Populate the table with data
        if last_ten_expenses:
            for expense in last_ten_expenses:
                # Ensure the tuple has at least 6 elements
                if len(expense) >= 6:
                    date_label = Label(text=expense[1], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # 'date'
                    person_label = Label(text=expense[2], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # 'person'
                    place_label = Label(text=expense[3], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # 'place'
                    amount_label = Label(text=str(expense[4]), size_hint_y=None, height=40, color=[1, 1, 1, 1])  # 'amount'
                    reason_label = Label(text=expense[6], size_hint_y=None, height=40, color=[1, 1, 1, 1])  # 'reason'

                    self.add_background(date_label)
                    self.add_background(person_label)
                    self.add_background(place_label)
                    self.add_background(amount_label)
                    self.add_background(reason_label)

                    grid_layout.add_widget(date_label)
                    grid_layout.add_widget(person_label)
                    grid_layout.add_widget(place_label)
                    grid_layout.add_widget(amount_label)
                    grid_layout.add_widget(reason_label)
                else:
                    print(f"Skipping expense: {expense} (not enough fields)")

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

        # Back button to return to the main screen
        back_button = Button(text='Back', size_hint=(0.1, 0.1), pos_hint={'right': 1, 'top': 1})
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
        self.app.root.current = 'main'  # Navigate back to the main screen
