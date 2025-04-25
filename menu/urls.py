from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.test, name='test-page'),
    path('api/products/<int:product_id>/', views.get_product_data, name='get_product_data'),
    ]