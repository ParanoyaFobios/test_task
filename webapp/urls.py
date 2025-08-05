from django.urls import path
from webapp import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('analytics/', views.analytics, name='analytics'),
    path('control-panel/', views.control_panel, name='control_panel'),  # Страница управления
    path('api/run-scraper/', views.run_scraper, name='run_scraper'),
]