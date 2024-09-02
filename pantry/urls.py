from django.contrib import admin
from django.urls import path, include
from pantry import views
from django.contrib.auth.decorators import login_required
from .views import GoogleAuthAPIView

urlpatterns = [
    path("", login_required(views.CafeHome.as_view()), name="home"),
    path("login/", views.login, name="login"),
    path("api/cart/", views.CartView.as_view(), name="cart"),
    path("api/google-auth/", GoogleAuthAPIView.as_view(), name="google_auth"),
    path(
        "api/delete-menu/<id>/delete/",
        login_required(views.UpdateCafeMenu.as_view()),
        name="delete_menu",
    ),
    path("cafe-menu/", login_required(views.CafeMenu.as_view()), name="mymenu"),
    path("cancel/", login_required(views.cancel), name="cancel"),
    path("contact/", login_required(views.CafeContact.as_view()), name="contact"),
    path(
        "create-checkout-session/<int:id>/",
        login_required(views.CreateCheckoutSessionView.as_view()),
        name="create-checkout-session",
    ),
    path("search/", login_required(views.SearchCafeMenu.as_view()), name="search"),
    path("success/", login_required(views.success), name="success"),
    path(
        "update_menu/<id>",
        login_required(views.UpdateCafeMenu.as_view()),
        name="update_menu",
    ),
    path(
        "webhooks/stripe/", login_required(views.stripe_webhook), name="stripe-webhook"
    ),
]
