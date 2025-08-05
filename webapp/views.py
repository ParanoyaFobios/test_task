from django.shortcuts import render
from webapp.models import Product
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.management import call_command
from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from django.db import models

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def analytics(request):
    # Простая аналитика - средняя цена товаров с рейтингом > 4
    high_rated_avg = Product.objects.filter(rating__gt=4).aggregate(models.Avg('current_price'))
    context = {
        'high_rated_avg': high_rated_avg['current_price__avg']
    }
    return render(request, 'analytics.html', context)

def control_panel(request):
    return render(request, 'control_panel.html')



@csrf_exempt  # Временно для тестов, в production используйте правильную CSRF защиту
@require_POST
def run_scraper(request):
    try:
        # Запускаем в отдельном потоке
        def run_command():
            call_command('scrape_amazon')
        
        Thread(target=run_command).start()
        return JsonResponse({'status': 'Парсинг запущен'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)