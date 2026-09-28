# The Cafe

A Django-based cafe management application that lets users browse menus, book tables, order food with Stripe payments, and search dishes via MongoDB text indexing.

## Features

- **User Authentication**: Google OAuth2 sign-in via django-allauth
- **Cafe Homepage**: View cafe details, contact form, and menu items
- **Menu Management**: Superusers can add, update, approve, and delete menu items
- **Table Booking**: Contact form for reservations
- **Search**: MongoDB text-indexed search across dish and category names
- **Shopping Cart**: Add, update, and remove items with ownership checks
- **Payments**: Stripe Checkout integration for card payments
- **Webhooks**: Stripe webhook handler for payment event processing

## Technologies

- **Backend**: Django 3.1, Django REST Framework, SimpleJWT
- **Databases**: MongoDB (menu search), PostgreSQL/MySQL/SQLite (primary)
- **Authentication**: django-allauth with Google OAuth2
- **Payments**: Stripe Checkout + Webhooks
- **Containerization**: Docker Compose

## Prerequisites

- Python 3.8+
- Docker & Docker Compose (for MongoDB)
- PostgreSQL/MySQL (or use SQLite for development)
- Google OAuth2 credentials
- Stripe account (test keys for development)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/namitha109tech/the-Cafe.git
cd the-cafe
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate        # Linux/macOS
# env\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env-sample .env
```

Edit `.env` with your actual values. At minimum you must set:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ALLOWED_HOSTS` | Comma-separated domains (e.g. `mycafe.com,www.mycafe.com`) |
| `DOMAIN` | Your cafe's public URL (e.g. `https://mycafe.com`) |
| `MONGO_ROOT_PASSWORD` | Password for MongoDB authentication |
| `STRIPE_SECRET_KEY` | Stripe secret key from dashboard |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook endpoint secret |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` | Google OAuth2 client ID |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` | Google OAuth2 client secret |

### 5. Start MongoDB with Docker Compose

```bash
docker-compose up -d mongodb
```

MongoDB is configured with authentication and is only accessible within the Docker network. The `MONGO_ROOT_USERNAME` defaults to `admin` and `MONGO_ROOT_PASSWORD` must be set.

### 6. Run database migrations

```bash
python manage.py migrate
```

### 7. Create a superuser (admin panel access)

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

### 9. Access the application

Open `http://127.0.0.1:8000` in your browser.

> **Note**: `DEBUG` is set to `False` by default in production settings. Set `DEBUG=True` only for local development by overriding in your `.env` or using a separate `settings_dev.py`.

## Docker Deployment

To run the full stack (web + migrations + MongoDB):

```bash
docker-compose up --build
```

The web service runs on port 8000. MongoDB is on an internal network and is not exposed externally.

## Project Structure

```
the-cafe/
├── the-cafe/                  # Django project settings
│   ├── settings.py            # Production settings (DEBUG=False by default)
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI entry point
│   └── asgi.py                # ASGI entry point
│
├── pantry/                    # Core Django app
│   ├── migrations/            # Database migrations
│   │   ├── 0001_initial.py
│   │   └── 0002_decimal_fields.py
│   ├── models.py              # Database models (AboutCafe, Menu, Category, Contact, Cart, CartItem)
│   ├── views.py               # Views (home, menu, cart, search, checkout, webhooks)
│   ├── urls.py                # App URL routes
│   ├── forms.py               # Django forms (MenuForm, ContactForm)
│   ├── serializers.py         # DRF serializers
│   ├── admin.py               # Admin panel registration
│   └── tests.py               # Unit tests
│
├── template/                  # HTML templates
│   ├── base.html              # Base template
│   ├── cafe.html              # Homepage with menu, contact form, Stripe JS
│   ├── login.html             # Google OAuth login
│   ├── suggestion_menu.html   # Menu suggestion page (superuser management)
│   ├── search_results.html    # Search results page
│   ├── success.html           # Stripe payment success
│   ├── cancel.html            # Stripe payment cancel
│   └── something_went_wrong.html  # Generic error page
│
├── static/                    # Static assets (CSS, images)
├── media/                     # User-uploaded files (menu photos)
├── logs/                      # Application error logs (created at runtime)
│
├── docker-compose.yml         # Docker Compose (MongoDB + web + migrations)
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env-sample                # Environment variable template
└── README.md                  # This file
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes | — | Django secret key for signing |
| `DEBUG` | No | `False` | Debug mode (never `True` in production) |
| `ALLOWED_HOSTS` | Yes | — | Comma-separated allowed hostnames |
| `DOMAIN` | Yes | — | Public domain of the cafe site |
| `MONGO_DB` | No | auto-built | MongoDB connection string |
| `MONGO_ROOT_USERNAME` | No | `admin` | MongoDB root username |
| `MONGO_ROOT_PASSWORD` | Yes | — | MongoDB root password |
| `STRIPE_PUBLIC_KEY` | Yes | — | Stripe publishable key |
| `STRIPE_SECRET_KEY` | Yes | — | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Yes | — | Stripe webhook signing secret |
| `STRIPE_CAFE_IMAGE` | Yes | — | URL of cafe logo for Stripe Checkout |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` | Yes | — | Google OAuth2 client ID |
| `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` | Yes | — | Google OAuth2 client secret |
| `SOCIAL_REST_GOOGLE_OAUTH2_URL` | Yes | — | Google userinfo endpoint URL |
| `DB_ENGINE` | No | — | Django DB engine (for non-MongoDB DB) |
| `DB_NAME` | No | — | Database name |
| `DB_USER` | No | — | Database user |
| `DB_PASSWORD` | No | — | Database password |
| `DB_HOST` | No | — | Database host |
| `LOGIN_URL` | No | `/login/` | Login redirect URL |
| `LOGIN_REDIRECT_URL` | No | `/` | Post-login redirect |
| `LOGOUT_URL` | No | `/logout/` | Logout URL |
| `LOGOUT_REDIRECT_URL` | No | `/` | Post-logout redirect |

## Security Notes

- `DEBUG` is `False` by default — all errors are logged server-side with generic messages returned to clients
- MongoDB requires authentication and is not exposed externally (Docker internal network only)
- All cart operations require authentication and enforce ownership checks
- All API views have rate limiting (30 req/min anonymous, 60 req/min authenticated)
- HTTPS is enforced with HSTS, secure cookies, and XSS protection headers
- Stripe webhook signature verification is enforced
- MongoDB search queries are sanitized to prevent injection
- Financial values use `DecimalField` (not `FloatField`) for precision

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please reach out at [developer@techversantinfo.com].
