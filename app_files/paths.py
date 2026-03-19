import os

# Project root = one level up from app_files/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# Ensure config folder exists
os.makedirs(CONFIG_DIR, exist_ok=True)

# Database & credentials
DATABASE_FILE = os.path.join(CONFIG_DIR, 'expense.db')
CREDENTIALS_FILE = os.path.join(CONFIG_DIR, 'credentials.json')

# Background images
BG_LOGIN = os.path.join(ASSETS_DIR, 'login_background.png')
BG_APP_1 = os.path.join(ASSETS_DIR, 'app_background_1.png')
BG_APP_2 = os.path.join(ASSETS_DIR, 'app_background_2.png')

# Font paths
FONT_CAMBO = os.path.join(FONTS_DIR, 'Cambo-Regular.ttf')
FONT_GARAMOND_EXTRABOLD = os.path.join(FONTS_DIR, 'EBGaramond-ExtraBold.ttf')
FONT_GARAMOND_ITALIC = os.path.join(FONTS_DIR, 'EBGaramond-Italic-VariableFont_wght.ttf')
FONT_DANCING = os.path.join(FONTS_DIR, 'DancingScript-Regular.ttf')