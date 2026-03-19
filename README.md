# 💰 Expense Tracker App

A personal expense tracking app built with Python and Kivy. Designed to run on desktop now, with plans to package it as an Android APK using Buildozer down the road.

Track your expenses by place, person, and reason — and keep an eye on your balances at a glance.

## ✨ Features

- **Login & Sign Up** — Simple credential-based authentication stored locally
- **Dashboard** — See all your balances grouped by place, with a running total
- **Add Transactions** — Log expenses with date, person, place, amount, and reason
- **View Transactions** — Browse your last 10 transactions in a clean table view
- **Multiple Places** — Add new places on the fly from the transaction screen
- **Auto Balance Calculation** — Balances update automatically when you add transactions
- **Custom Backgrounds** — Each screen has its own gradient background with contrast-optimized font colors

## 📁 Project Structure

```
expanse_app/
├── app_files/
│   ├── main.py                 # App entry point
│   ├── paths.py                # Centralized path management
│   ├── database.py             # SQLite database operations
│   ├── login.py                # Login & sign up screen
│   ├── layout.py               # Main dashboard screen
│   ├── add_transaction.py      # Add transaction screen
│   └── view_transactions.py    # View transactions screen
├── assets/                     # Background images
│   ├── login_background.png
│   ├── app_background_1.png
│   └── app_background_2.png
├── fonts/                      # Custom fonts (Cambo, EB Garamond, Dancing Script, etc.)
├── config/                     # Auto-generated at runtime (database + credentials)
├── LICENSE
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/khan022/expanse_app.git
   cd expanse_app
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

   Activate it:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install kivy
   ```

4. **Run the app**
   ```bash
   python app_files/main.py
   ```

5. **Sign up** on the login screen with any email/password — this creates your local credentials. Then log in and start tracking!

## 🛠️ Tech Stack

- **Python** — Core language
- **Kivy** — Cross-platform UI framework
- **SQLite** — Local database (no server needed)
- **Custom fonts** — Cambo, EB Garamond, Dancing Script, Roboto

## 🗺️ Roadmap

- [ ] Package as Android APK using Buildozer
- [ ] Add expense categories and filtering
- [ ] Charts and spending summaries
- [ ] Export data to CSV
- [ ] Password hashing for better security
- [ ] Multi-user support

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

Made with ☕ by [Shafkat Khan Siam](https://github.com/khan022)