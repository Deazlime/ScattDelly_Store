from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True)
    images = models.JSONField(default=list, blank=True, null=True)  # список путей к изображениям
    specifications = models.JSONField(default=list, blank=True)  # [{"name": ..., "value": ...}]
    is_hit = models.BooleanField(default=False)
    is_sale = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    sales_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # Добавьте нужные поля (user, status, total и т.д.)

    def __str__(self):
        return f"Order #{self.id}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=10, blank=True, choices=[('male', 'Мужской'), ('female', 'Женский'), ('other', 'Другой')], verbose_name='Пол')
    subscribe_news = models.BooleanField(default=False, verbose_name='Согласен на рассылку')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    def __str__(self):
        return f'{self.user.username} ({self.phone})'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.PositiveSmallIntegerField()
    pros = models.TextField(blank=True)
    cons = models.TextField(blank=True)
    comment = models.TextField()
    photos = models.ImageField(upload_to='reviews/photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
