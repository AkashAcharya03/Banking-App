# Banking Web Application

This is a comprehensive banking web application designed for account management, secure fund transfers, bill payments, transaction history and bill history tracking. It provides an easy-to-use interface for users to manage their finances effectively.

## Table of Contents

- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Technologies Used

- **Frontend**: HTML, CSS (Bootstrap for responsiveness)
- **Backend**: Django
- **Database**: MySQL
- **Python**: For backend logic and data handling

## Features

- **User Authentication**: Secure sign-up, login, and session management for users.
- **Account Management**: View and manage user account details.
- **Fund Transfer**: Transfer money securely between accounts.
- **Bill Payment**: Pay bills and view payment history.
- **Transaction History**: Track all user transactions with detailed records.
- **Bill History**: Track all user bill transactions with detailed records.

## Installation

Follow these steps to get the application up and running:

1. Clone the repository:
    ```bash
    https://github.com/AkashAcharya03/Banking-App.git
    ```

2. Navigate into the project directory:
    ```bash
    cd banking-app/banking
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Install MySQL and set up the database. You can use the following commands to create a database:
    ```sql
    CREATE DATABASE banking_db;
    ```

6. Update the `DATABASES` setting in `settings.py` to use MySQL:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'banking_db',
            'USER': 'your_mysql_username',
            'PASSWORD': 'your_mysql_password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

7. Run migrations to set up the database:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

8. Start the development server:
    ```bash
    python manage.py runserver
    ```

9. Access the application by visiting `http://127.0.0.1:8000/` in your web browser.



## Usage

Once the application is running, you can:

- **Sign Up**: Create a new account by filling in your details on the `signup.html` page.
- **Log In**: Use your credentials to log in through the `signin.html` page.
- **Manage Account**: View and update your account details.
- **Fund Transfer**: Transfer money to other users using the `transfer.html` page.
- **Pay Bills**: Access the bill payment feature through the `bill_payment.html` page.
- **View Transaction History**: Check your transaction records on the `transaction_history.html` page.

