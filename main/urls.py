from django.urls import path
from . import views
from main.admin import custom_admin_site
from .views import admin_dashboard, ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView, UserListAPIView, ReviewListAPIView, CategoryListAPIView

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', views.index, name='index'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('calculator/', views.calculator_view, name='calculator'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/products/', ProductListCreateAPIView.as_view(), name='api_products'),
    path('api/products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='api_product_detail'),
    path('captcha/refresh/', views.captcha_refresh, name='captcha_refresh'),
    path('api/users/', UserListAPIView.as_view(), name='api_users'),
    path('api/reviews/', ReviewListAPIView.as_view(), name='api_reviews'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('profile/', views.profile_view, name='profile'),
    path('api/categories/', CategoryListAPIView.as_view(), name='api_categories'),
]
