from django.urls import path
from webapp import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('analytics/', views.analytics, name='analytics'),
]