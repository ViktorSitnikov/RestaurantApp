from django.shortcuts import render
from .models import Category, Dishes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from cart.models import Cart, CartItem
from orders.models import Order

def index(request):
    categories = Category.objects.prefetch_related('products').all()
    all_products = Dishes.objects.prefetch_related('category').all()
    novelty_products = Dishes.objects.filter(is_new=True)
    hit_products = Dishes.objects.filter(is_hit=True)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.dishes.price * item.quantity for item in cart_items)

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.dishes.price * item.quantity for item in cart_items)

    active_order = None
    if request.user.is_authenticated:
        active_order = Order.objects.filter(user=request.user, status='Готовится').first()

    return render(request, 'menu/index.html', {
        'active_order': active_order,
        'categories': categories,
        'all_products': all_products,
        'novelty_products': novelty_products,
        'hit_products': hit_products,
        'cart_items': cart_items,
        'total_price': total_price,
    })

def test(request):
    categories = Category.objects.prefetch_related('products').all()
    all_products = Dishes.objects.prefetch_related('category').all()
    novelty_products = Dishes.objects.filter(is_new=True)
    hit_products = Dishes.objects.filter(is_hit=True)
    return render(request, 'menu/test.html', {
        'categories': categories,
        'all_products': all_products,
        'novelty_products': novelty_products,
        'hit_products': hit_products,
    })

def get_product_data(request, product_id):
    product = get_object_or_404(Dishes, id=product_id)
    data = {
        'name': product.name,
        'photolink': product.photolink,
        'description': product.description,
        'price': product.price,
        'grams': str(product.grams),
        'structure': product.structure,
        'kalories': str(product.kalories),
        'protein': str(product.protein),
        'fat': str(product.fat),
        'carbohydrates': str(product.carbohydrates),
        'category': product.category.name,
    }

    return JsonResponse(data)
