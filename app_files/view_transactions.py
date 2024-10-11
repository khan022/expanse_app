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

        with self.canvas.before:
            self.bg_image = Image(source='../Expense app/possible_bg2.jpg', allow_stretch=True, keep_ratio=False)
            self.add_widget(self.bg_image)

        top_padding = FloatLayout(size_hint=(1, 0.1))  
        self.add_widget(top_padding)

        header_layout = GridLayout(cols=5, size_hint=(1, 0.1), pos_hint={'top': 0.9}, padding=[10, 10], spacing=10)

        headers = ['Date', 'Person', 'Place', 'Amount', 'Reason']
        for header in headers:
            header_label = Label(text=header, font_size=20, font_name='../fonts/Cambo-Regular.ttf', bold=True, size_hint_y=None, height=40, color=[1, 1, 1, 1])
            self.add_background(header_label)
            header_layout.add_widget(header_label)

        self.add_widget(header_layout)

        scroll_view = ScrollView(size_hint=(1, 0.7), pos_hint={'x': 0, 'y': 0.1})
        grid_layout = GridLayout(cols=5, size_hint_y=None, padding=[10, 10], spacing=10)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        last_ten_expenses = self.app.get_last_ten_expenses()
        places = self.app.get_unique_places()

        # print(places)

        if last_ten_expenses:
            for expense in last_ten_expenses:
                if len(expense) >= 6:
                    date_label = Label(text=expense[1], font_size=15, font_name='../fonts/Cambo-Regular.ttf', size_hint_y=None, height=40, color=[1, 1, 1, 1]) 
                    person_label = Label(text=expense[2], font_size=15, font_name='../fonts/Cambo-Regular.ttf', size_hint_y=None, height=40, color=[1, 1, 1, 1]) 
                    place_label = Label(text=expense[3], font_size=15, font_name='../fonts/Cambo-Regular.ttf', size_hint_y=None, height=40, color=[1, 1, 1, 1])  
                    amount_label = Label(text=str(expense[4]), font_size=15, font_name='../fonts/Cambo-Regular.ttf', size_hint_y=None, height=40, color=[1, 1, 1, 1]) 
                    reason_label = Label(text=expense[6], font_size=15, font_name='../fonts/Cambo-Regular.ttf', 
                                    size_hint_y=None, height=40, size_hint_x=None, width=150, color=[1, 1, 1, 1],
                                    text_size=(150, None), halign='center', valign='middle')

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

        scroll_view.add_widget(grid_layout)
        self.add_widget(scroll_view)

        back_button = Button(text='⬇', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.5, 'y': 0},
                                    background_normal='', background_color=[0, 0, 0, 0])
        back_button.bind(on_press=self.go_back)
        self.add_widget(back_button)

    def add_background(self, widget):
        with widget.canvas.before:
            Color(0, 0, 0, 0.86) 
            widget.rect = Rectangle(size=widget.size, pos=widget.pos)
            widget.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def go_back(self, instance):
        self.app.root.current = 'main'
