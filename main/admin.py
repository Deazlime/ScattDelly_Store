from django.contrib import admin
from django.urls import path
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Product, Order, Category

class CustomAdminSite(admin.AdminSite):
    index_template = "admin/base_site.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_view(self.dashboard), name='index'),
        ]
        return custom_urls + urls

    def dashboard(self, request):
        User = get_user_model()
        context = self.each_context(request)
        context.update({
            "products_count": Product.objects.count(),
            "users_count": User.objects.count(),
            "orders_count": Order.objects.count(),
            "last_products": Product.objects.order_by('-created_at')[:5],
            "last_orders": Order.objects.order_by('-created_at')[:5],
        })
        return render(request, "admin/base_site.html", context)

custom_admin_site = CustomAdminSite()
custom_admin_site.register(Product)
custom_admin_site.register(Order)
custom_admin_site.register(Category)
