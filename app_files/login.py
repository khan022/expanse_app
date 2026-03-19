import os
import json
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from paths import CREDENTIALS_FILE, BG_LOGIN, FONT_CAMBO, CONFIG_DIR

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

        # Background setup - login_background.png (purple/pink/blue gradient)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_image = Rectangle(source=BG_LOGIN, size=self.size)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widgets()

    def _update_rect(self, *args):
        self.bg_image.pos = self.pos
        self.bg_image.size = self.size

    def add_widgets(self):
        # Container for the main layout
        layout_container = BoxLayout(
            orientation='vertical',
            padding=[30, 40, 30, 300],
            spacing=40,
            size_hint=(0.8, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Two-column layout for email and password fields
        field_container = BoxLayout(
            orientation='horizontal',
            spacing=20,
            size_hint_y=None,
            height=120
        )

        # Column 1: Labels with semi-transparent background
        label_container = BoxLayout(
            orientation='vertical',
            spacing=20
        )

        # Email Label - bright cyan for contrast against purple/pink bg
        email_label = Label(
            text='Email:', 
            font_size=20, 
            font_name=FONT_CAMBO, 
            color=(0.4, 1, 1, 1),
            size_hint_y=None,
            height=50,
            padding=(10, 10),
        )
        with email_label.canvas.before:
            Color(0, 0, 0, 0.5)
            self.bg_email = Rectangle(pos=email_label.pos, size=email_label.size)

        email_label.bind(pos=lambda instance, value: setattr(self.bg_email, 'pos', value))
        email_label.bind(size=lambda instance, value: setattr(self.bg_email, 'size', value))

        # Password Label
        password_label = Label(
            text='Password:', 
            font_size=20, 
            font_name=FONT_CAMBO, 
            color=(0.4, 1, 1, 1),
            size_hint_y=None,
            height=50,
            padding=(10, 10),
        )
        with password_label.canvas.before:
            Color(0, 0, 0, 0.5)
            self.bg_password = Rectangle(pos=password_label.pos, size=password_label.size)

        password_label.bind(pos=lambda instance, value: setattr(self.bg_password, 'pos', value))
        password_label.bind(size=lambda instance, value: setattr(self.bg_password, 'size', value))

        label_container.add_widget(email_label)
        label_container.add_widget(password_label)

        # Column 2: Input fields
        input_container = BoxLayout(
            orientation='vertical',
            spacing=20
        )

        # Email field
        self.email_input = TextInput(
            hint_text="Enter Email",
            multiline=False,
            background_normal='',  
            background_color=(0, 0, 0, 0.4),  
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            halign='center',
            size_hint_y=None,
            height=50,
            font_name=FONT_CAMBO,
            padding_y=(12, 12)
        )

        # Password field
        self.password_input = TextInput(
            hint_text="Enter Password",
            multiline=False,
            background_normal='',  
            background_color=(0, 0, 0, 0.4),  
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            halign='center',
            password=True,  
            size_hint_y=None,
            height=50,
            font_name=FONT_CAMBO,
            padding_y=(12, 12)
        )

        input_container.add_widget(self.email_input)
        input_container.add_widget(self.password_input)

        field_container.add_widget(label_container)
        field_container.add_widget(input_container)

        # Horizontal layout for buttons
        button_container = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )

        # Login button - soft blue-green to complement purple bg
        login_button = Button(
            text='Login', 
            font_size=20, 
            font_name=FONT_CAMBO, 
            background_color=(0.1, 0.6, 0.8, 0.9),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_down=''
        )
        login_button.bind(on_press=self.login)

        # Signup button - warm pink to match bg gradient
        signup_button = Button(
            text='Sign Up', 
            font_size=20, 
            font_name=FONT_CAMBO, 
            background_color=(0.7, 0.15, 0.4, 0.9),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
            background_normal='',
            background_down=''
        )
        signup_button.bind(on_press=self.sign_up)

        button_container.add_widget(login_button)
        button_container.add_widget(signup_button)

        layout_container.add_widget(field_container)
        layout_container.add_widget(button_container)

        self.add_widget(layout_container)

    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if self.validate_credentials(email, password):
            self.clear_fields()
            self.app.root.current = 'main'
        else:
            self.show_popup("Login Failed", "Invalid email or password. Please try again.")

    def validate_credentials(self, email, password):
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                credentials = json.load(f)
                stored_email = credentials.get('email')
                stored_password = credentials.get('password')
                return email == stored_email and password == stored_password
        return False

    def sign_up(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if email and password:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            with open(CREDENTIALS_FILE, 'w') as f:
                json.dump({'email': email, 'password': password}, f)
            self.show_popup("Sign Up Successful", "You can now log in with your credentials.")
            self.clear_fields()
        else:
            self.show_popup("Sign Up Failed", "Please enter a valid email and password.")

    def clear_fields(self):
        self.email_input.text = ''
        self.password_input.text = ''

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        dismiss_button = Button(
            text='Dismiss', 
            size_hint=(0.5, 0.2),
            pos_hint={'center_x': 0.5}
        )

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(dismiss_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        dismiss_button.bind(on_press=popup.dismiss)
        popup.open()