from django.shortcuts import render
from .models import Category, Dishes

def index(request):
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
