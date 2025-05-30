from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from menu.models import Dishes
from accounts.forms import ProfileForm
from orders.forms import OrderForm

def ensure_single_cart(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        carts = Cart.objects.filter(session_key=session_key, user__isnull=True)
    
    if carts.count() > 1:
        main_cart = carts.first()
        for extra_cart in carts.exclude(id=main_cart.id):
            for item in extra_cart.cartitem_set.all():
                main_item, created = CartItem.objects.get_or_create(
                    cart=main_cart,
                    dishes=item.dishes,
                    defaults={'quantity': item.quantity}
                )
                if not created:
                    main_item.quantity += item.quantity
                    main_item.save()
            extra_cart.delete()
        return main_cart
    elif carts.exists():
        return carts.first()
    else:
        if request.user.is_authenticated:
            return Cart.objects.create(user=request.user)
        else:
            return Cart.objects.create(session_key=session_key)

def cart_page(request):
    cart = ensure_single_cart(request)
    profileForm = ProfileForm(instance=request.user if request.user.is_authenticated else None)
    orderForm = OrderForm()


    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.dishes.price * item.quantity for item in cart_items)
    
    return render(request, 'cart/cart_page.html', {
        'cart_id': cart.id,
        'cart_items': cart_items,
        'total_price': total_price,
        'profile_form': profileForm,
        'order_form': orderForm,
    })