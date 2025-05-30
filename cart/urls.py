from django.urls import path
from . import views, api_views
app_name = 'cart'

urlpatterns = [
    path('api/cart/', api_views.get_cart_api, name='get_cart_api'),
    path('api/cart/add/<int:dish_id>/', api_views.add_to_cart_api, name='add_to_cart_api'),
    path('api/cart/remove/<int:dish_id>/', api_views.remove_from_cart_api, name='remove_from_cart_api'),
    
    
    # path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    # path('remove_from_cart/<int:dish_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/', views.cart_page, name='cart-page'),

]
