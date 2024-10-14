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
            Color(1, 1, 1, 1)  # White background
            self.bg_image = Rectangle(source='../Expense app/possible_bg2.jpg', size=self.size)

        self.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widgets()

    def _update_rect(self, *args):
        # Update background rectangle to fit the layout
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

        # Email Label with semi-transparent background
        email_label = Label(
            text='Email:', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
            padding=(10, 10),
        )
        # Semi-transparent background for email label
        with email_label.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black
            self.bg_email = Rectangle(pos=email_label.pos, size=email_label.size)

        # Bind position and size of rectangle to label's position and size
        email_label.bind(pos=lambda instance, value: setattr(self.bg_email, 'pos', value))
        email_label.bind(size=lambda instance, value: setattr(self.bg_email, 'size', value))

        # Password Label with semi-transparent background
        password_label = Label(
            text='Password:', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
            padding=(10, 10),
        )
        # Semi-transparent background for password label
        with password_label.canvas.before:
            Color(0, 0, 0, 0.5)  # Semi-transparent black
            self.bg_password = Rectangle(pos=password_label.pos, size=password_label.size)

        # Bind position and size of rectangle to label's position and size
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
            background_color=(1, 1, 1, 0.8),  
            foreground_color=(0, 0, 0, 1),
            halign='center',
            size_hint_y=None,
            height=50,
            font_name='../fonts/Cambo-Regular.ttf',
            padding_y=(12, 12)  # For better vertical alignment
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

        input_container.add_widget(self.email_input)
        input_container.add_widget(self.password_input)

        # Add label and input containers to field container
        field_container.add_widget(label_container)
        field_container.add_widget(input_container)

        # Horizontal layout for buttons
        button_container = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
            height=50
        )

        # Login button
        login_button = Button(
            text='Login', 
            font_size=20, 
            font_name='../fonts/Cambo-Regular.ttf', 
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50,
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
            size_hint=(1, None),
            height=50,
            background_normal='',  # Remove default background
            background_down=''
        )
        signup_button.bind(on_press=self.sign_up)

        # Add buttons to button container
        button_container.add_widget(login_button)
        button_container.add_widget(signup_button)

        # Add field container and button container to the main layout
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
            self.clear_fields()
        else:
            self.show_popup("Sign Up Failed", "Please enter a valid email and password.")

    def clear_fields(self):
        # Clear email and password fields
        self.email_input.text = ''
        self.password_input.text = ''

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10)
        popup_label = Label(text=message)
        dismiss_button = Button(
            text='Dismiss', 
            size_hint=(0.5, 0.2),  # Adjust the width
            pos_hint={'center_x': 0.5}  # Center the button horizontally
        )

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(dismiss_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        dismiss_button.bind(on_press=popup.dismiss)
        popup.open()

