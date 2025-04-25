from django.urls import path
from .views import login_view, register, custom_logout, profile

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout'),
    path('profile/', profile, name='profile'),
]