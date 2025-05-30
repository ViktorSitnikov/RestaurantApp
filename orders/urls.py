from django.urls import path, include
from . import api_views, views

app_name = 'orders'

urlpatterns = [
    path('confirm-order/', api_views.checkout, name='confirm-order'),



    path('orders/', views.order_page, name='order-page'),
    path('orders/confirm/', views.confirm_order_modal, name='confirm_order_modal'),
]