# view_transactions.py
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

class ViewTransactionsLayout(FloatLayout):
    def __init__(self, app, **kwargs):
        super(ViewTransactionsLayout, self).__init__(**kwargs)
        self.app = app

        # Create a ScrollView to display transactions
        scroll_view = ScrollView(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        grid_layout = GridLayout(cols=2, size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # Fetch last 10 expenses
        last_ten_expenses = self.app.get_last_ten_expenses()

        # Create headers
        grid_layout.add_widget(Label(text='Place', bold=True, size_hint_y=None, height=40))
        grid_layout.add_widget(Label(text='Amount', bold=True, size_hint_y=None, height=40))

        if last_ten_expenses:
            for expense in last_ten_expenses:
                place_label = Label(text=expense[2], size_hint_y=None, height=40)  # Assuming 'place' is at index 2
                amount_label = Label(text=str(expense[4]), size_hint_y=None, height=40)  # Assuming 'amount' is at index 4

                grid_layout.add_widget(place_label)
                grid_layout.add_widget(amount_label)

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

        # Back button to return to the main screen
        back_button = Button(text='Back', size_hint=(0.1, 0.1), pos_hint={'right': 1, 'top': 1})
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def go_back(self, instance):
        """ Go back to the main screen. """
        self.app.root.current = 'main'  # Navigate back to the main screen
