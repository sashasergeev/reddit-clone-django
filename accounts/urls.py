from django.urls import path, include
from .views import register, LoginView, LogoutView

app_name = "accounts"
urlpatterns = [
    path('login/', LoginView, name="login"),
    path('register/', register, name="register"),
    path('logout/', LogoutView, name="logout")
]