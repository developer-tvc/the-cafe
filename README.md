
# The Cafe

## Overview

This is a web-based application built using Django that allows users to book tables at a cafe. 
The application provides features for user authentication, café selection, time slot booking, 
search, and ordering food from the suggested food menu. The payment gateway for ordering food.

## Features

- **User Authentication**: Secure login and registration system using Google auth token.
- **Booking System**: Users can choose a date and time to book a table with some people.
- **Suggest Dishes for Cafe Menu**: Users can view, update, or delete menu dishes they suggested.
- **Admin Panel**: Administrators can manage café, view bookings, and handle the menu.
- **Search Menu Dishes**: Users can search menu dishes based on category and dish names.
- **Order food using menu**: Users can view the menu, order dishes, and pay payments using stripe payment gateway using debit/credit cards.

## Technologies Used

- **Backend**: Django (Python)
- **Database**: MongoDB (default), can be configured to use PostgreSQL, MySQL, SQLite, etc.
- **Frontend**: HTML, CSS, Bootstrap (or any other framework you used)
- **Authentication**: Django's built-in authentication system and Google authentication.

## Installation

### Prerequisites

- Python 3. x
- Django 3.x or 4.x
- pip (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/namitha109tech/the-Cafe.git
   cd cafe-booking-app
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scriptsactivate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add environment variables**:
   ```bash
   cp .env-sample .env
   ```
   Fill the constants with actual values

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for accessing the admin panel):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   Open your browser and go to `http://127.0.0.1:8000`.

## Usage

### User Guide

1. **Register/Login**: Users can register or log in to their accounts.
2. **Browse Café**: After logging in, users can browse through available café.
3. **Book a Table**: Users can select a café, choose a date and time, and book a table.
4. **Suggest Dishes for Cafe Menu**: Users can view, update, or delete menu dishes they suggested.
5. **Search Menu Dishes**: Users can search menu dishes based on category and dish names.
6. **Order food using menu**: Users can view the menu, order dishes, and pay payments using the Stripe payment gateway using debit/credit cards.

### Admin Guide

1. **Admin Panel**: Access the admin panel by going to `http://127.0.0.1:8000/admin` and logging in with the superuser credentials.
2. **Manage Café**: Admins can add, update, or delete café details.
3. **View Bookings**: Admins can view all user bookings.
4. **Handle menu**: Handle menu details and update their availability.

## Project Structure

```plaintext
the-cafe/
│
├── the-cafe/                # Main Django project directory.
│   ├── settings.py         # Django settings.
│   ├── urls.py             # URL routing.
│   └── wsgi.py             # WSGI configuration.
|   └── asgi.py             # ASGI configuration.
│
├── pantry/               # Django app for managing menu items.
│   ├── migrations/         # Database migrations.
│   ├── models.py           # Database models.
│   ├── views.py            # Views for handling requests.
│   ├── urls.py             # URLs specific to this app.
|   |__ forms.py	          # various types of forms. 
|   |__ serializers.py	    # Serializer for connecting Database and View.
│
├── media/
|    |__thumbnails          # Django app for managing user media and related images.
|── templates/              # HTML templates.
|__ static/                 # Static files for  HTML, CSS, and JS.
|
|__ docker-compose.yml      #Docker compose file for docker.
|
|__ pantry.json           # Database data in JSON format.
|
├── manage.py               # Django's command-line utility.
├── requirements.txt        # Python dependencies.
└── README.md               # Project documentation.
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please reach out to [developer@techversantinfo.com].
