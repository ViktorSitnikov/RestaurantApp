from django.shortcuts import render
from .models import Order
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt # Временно для тестирования, лучше использовать csrf_protect

def order_page(request):
    return render(request, 'orders/confirm-order.html')

def confirm_order_modal(request):
    
    return render(request, 'orders/confirm-order.html')

def order_management_view(request):
    accepted_orders = Order.objects.filter(status='Готовится').order_by('-created_at')
    completed_orders = Order.objects.filter(status='Выполнен').order_by('-created_at')
    context = {
        'accepted_orders': accepted_orders,
        'completed_orders': completed_orders,
    }
    return render(request, 'orders/order_management.html', context)

@csrf_exempt # Временно для тестирования
@require_POST
def update_order_status(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
        new_status = request.POST.get('status')
        
        # Проверяем, является ли новый статус допустимым
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status and new_status in valid_statuses:
            order.status = new_status
            order.save()
            return JsonResponse({'status': 'success', 'new_status': order.status})
        else:
            return JsonResponse({'status': 'error', 'message': 'Недопустимый статус'}, status=400)
    except Order.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Заказ не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
