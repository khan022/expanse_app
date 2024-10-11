import os
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

class LoginScreen(Screen):
    def __init__(self, app, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.app = app
        self.layout = LoginLayout(app)
        self.add_widget(self.layout)

class LoginLayout(BoxLayout):
    def __init__(self, app, **kwargs):
        super(LoginLayout, self).__init__(**kwargs)
        self.app = app
        self.orientation = 'vertical'

        # Background setup
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_image = Rectangle(source='../Expense app/possible_bg2.jpg', pos=self.pos, size=self.size)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widgets()

    def _update_rect(self, *args):
        self.bg_image.pos = self.pos
        self.bg_image.size = self.size

    def add_widgets(self):
        # Container for central layout
        layout_container = BoxLayout(
            orientation='vertical',
            padding=[30, 40, 30, 40],
            spacing=40,  # To adjust the gap between widgets
            size_hint=(0.8, 0.9), 
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Email field
        self.email_input = TextInput(
            hint_text="Enter Email",
            multiline=False,
            background_normal='',  
            background_color=(1, 1, 1, 0.8),  
            foreground_color=(0, 0, 0, 1),
            halign='center',
            size_hint_y=None,
            height=50,
            font_name='../fonts/Cambo-Regular.ttf',
            padding_y=(12, 12)  # For better vertical alignment
        )
        email_label = Label(
            text='Email:', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=30
        )

        # Password field
        self.password_input = TextInput(
            hint_text="Enter Password",
            multiline=False,
            background_normal='',  
            background_color=(1, 1, 1, 0.8),  
            foreground_color=(0, 0, 0, 1),
            halign='center',
            password=True,  
            size_hint_y=None,
            height=50,
            font_name='../fonts/Cambo-Regular.ttf',
            padding_y=(12, 12)
        )
        password_label = Label(
            text='Password:', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=30
        )

        # Login button
        login_button = Button(
            text='Login', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
            height=10,
            background_normal='',  # Remove default background
            background_down=''  # Remove click background
        )
        login_button.bind(on_press=self.login)

        # Signup button
        signup_button = Button(
            text='Sign Up', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2),
            height=10,
            background_normal='',  # Remove default background
            background_down=''
        )
        signup_button.bind(on_press=self.sign_up)

        # layout_container.padding = [20, 20, 20, 80]

        # Add widgets to the layout
        layout_container.add_widget(email_label)
        layout_container.add_widget(self.email_input)
        layout_container.add_widget(password_label)
        layout_container.add_widget(self.password_input)
        # layout_container.add_widget(padding)
        layout_container.add_widget(login_button)
        layout_container.add_widget(signup_button)

        self.add_widget(layout_container)

    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if self.validate_credentials(email, password):
            self.app.root.current = 'main'
        else:
            self.show_popup("Login Failed", "Invalid email or password. Please try again.")

    def validate_credentials(self, email, password):
        credentials_file = os.path.join('../config', 'credentials.json')
        if os.path.exists(credentials_file):
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
                stored_email = credentials.get('email')
                stored_password = credentials.get('password')
                return email == stored_email and password == stored_password
        return False

    def sign_up(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if email and password:
            credentials_file = os.path.join('../config', 'credentials.json')
            with open(credentials_file, 'w') as f:
                json.dump({'email': email, 'password': password}, f)
            self.show_popup("Sign Up Successful", "You can now log in with your credentials.")
        else:
            self.show_popup("Sign Up Failed", "Please enter a valid email and password.")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()
