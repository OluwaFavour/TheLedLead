from django.urls import path
from .views import index, admin_login

urlpatterns = [
    path('', index, name='admin-index'),
    path('login/', admin_login, name='admin-login'),
]