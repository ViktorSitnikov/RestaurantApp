from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CartItem, Cart, Dishes
from .serializers import CartItemSerializer

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

@api_view(['GET'])
def get_cart_api(request):
    cart = ensure_single_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart_api(request, dish_id):
    try:
        dish = Dishes.objects.get(id=dish_id)
    except Dishes.DoesNotExist:
        return Response({'error': 'Блюдо не найдено'}, status=404)
    
    cart = ensure_single_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, dishes=dish)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return Response({'success': True})

@api_view(['POST'])
def remove_from_cart_api(request, dish_id):
    completely = request.data.get('completely', False)
    
    try:
        dish = Dishes.objects.get(id=dish_id)
    except Dishes.DoesNotExist:
        return Response({'error': 'Блюдо не найдено'}, status=404)
    
    cart = ensure_single_cart(request)
    cart_item = CartItem.objects.filter(cart=cart, dishes=dish).first()

    if cart_item:
        if completely:
            cart_item.delete()
        elif cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return Response({'success': True})