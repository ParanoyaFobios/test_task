from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=500, null=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    rating = models.FloatField(null=True)
    reviews = models.IntegerField(null=True)  # Изменил на Integer для количества отзывов
    product_url = models.URLField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавим дату создания
    
    class Meta:
        ordering = ['-created_at']  # Сортировка по дате создания
        
    def __str__(self):
        return self.title[:50]  # Возвращаем первые 50 символов названия