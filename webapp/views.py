from django.shortcuts import render
from webapp.models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'webapp/product_list.html', {'products': products})

def analytics(request):
    # Простая аналитика - средняя цена товаров с рейтингом > 4
    high_rated_avg = Product.objects.filter(rating__gt=4).aggregate(models.Avg('current_price'))
    context = {
        'high_rated_avg': high_rated_avg['current_price__avg']
    }
    return render(request, 'webapp/analytics.html', context)