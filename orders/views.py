from django.shortcuts import render

def order_page(request):
    return render(request, 'orders/confirm-order.html')

def confirm_order_modal(request):
    
    return render(request, 'orders/confirm-order.html')
