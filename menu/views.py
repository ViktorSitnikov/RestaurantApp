from django.shortcuts import render
from .models import Category, Dishes
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def index(request):
    categories = Category.objects.prefetch_related('products').all()
    all_products = Dishes.objects.prefetch_related('category').all()
    novelty_products = Dishes.objects.filter(is_new=True)
    hit_products = Dishes.objects.filter(is_hit=True)
    return render(request, 'menu/index.html', {
        'categories': categories,
        'all_products': all_products,
        'novelty_products': novelty_products,
        'hit_products': hit_products,
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
        'carbohydrates': str(product.carbohydrates)
    }

    return JsonResponse(data)
