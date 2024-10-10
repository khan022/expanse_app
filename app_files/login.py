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
        # Main layout for input fields
        layout_container = BoxLayout(
            orientation='vertical',
            padding=[35, 80, 35, 80],
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
            height=40,
            font_name='../fonts/Cambo-Regular.ttf',
        )
        layout_container.add_widget(Label(text='Email:', font_size=20, 
                                    font_name='../fonts/Cambo-Regular.ttf'))
        layout_container.add_widget(self.email_input)

        # Password field
        self.password_input = TextInput(
            hint_text="Enter Password",
            multiline=False,
            background_normal='',  
            background_color=(1, 1, 1, 0.8),  
            foreground_color=(0, 0, 0, 1),
            halign='center',
            password=True,  # Password masking
            size_hint_y=None,
            height=40,
            font_name='../fonts/Cambo-Regular.ttf',
        )
        layout_container.add_widget(Label(text='Password:', font_size=20, 
                                    font_name='../fonts/Cambo-Regular.ttf'))
        layout_container.add_widget(self.password_input)

        # Login button
        login_button = Button(text='Login', font_size=20, font_name='../fonts/Cambo-Regular.ttf', 
                                size_hint=(1, 0.1))
        login_button.bind(on_press=self.login)
        layout_container.add_widget(login_button)

        # Signup button
        signup_button = Button(text='Sign Up', font_size=20, font_name='../fonts/Cambo-Regular.ttf', 
                                size_hint=(1, 0.1))
        signup_button.bind(on_press=self.sign_up)
        layout_container.add_widget(signup_button)

        self.add_widget(layout_container)

    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if self.validate_credentials(email, password):
            # Credentials are valid, switch to the main app
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
