from rest_framework.decorators import api_view
from rest_framework.response import Response
from cart.models import CartItem
from .models import Order, OrderItem
from menu.models import Dishes
from cart.views import ensure_single_cart  # уже у тебя есть
from django.db import transaction

@api_view(['POST'])
def checkout(request):
    cart = ensure_single_cart(request)
    items = CartItem.objects.filter(cart=cart)

    if not items.exists():
        return Response({'error': 'Корзина пуста'}, status=400)

    # Получаем имя/фамилию/комментарий из запроса
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    comment = request.data.get('comment')

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            comment=comment
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                dish=item.dishes,
                quantity=item.quantity,
                price=item.dishes.price
            )

        # Очищаем корзину
        items.delete()

    return Response({'success': True, 'order_id': order.id})