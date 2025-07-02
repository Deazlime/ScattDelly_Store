from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, UserSerializer, ReviewSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import RegisterForm, LoginForm, ReviewForm, ProfileForm
from .utils import generate_captcha_text, generate_captcha_image
from django.contrib.auth.models import User
from .models import UserProfile, ProductImage, Review
from rest_framework.permissions import IsAdminUser
import os

# Create your views here.

def index(request):
    popular_products = Product.objects.order_by('-sales_count')[:4]
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'main/index.html', {
        'popular_products': popular_products,
        'cart_count': cart_count,
    })

def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'cart_count': sum(cart.values())})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    for product in products:
        cart_items.append({
            'product': product,
            'quantity': cart[str(product.id)],
        })
    return render(request, 'main/cart.html', {
        'cart_items': cart_items,
        'cart_count': sum(cart.values()),
    })

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalog')
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        captcha_input = request.POST.get('captcha', '').upper()
        captcha_session = request.session.get('captcha_text', '')
        login_input = request.POST.get('username')
        password = request.POST.get('password')
        user = None
        # Проверка капчи
        if captcha_input != captcha_session:
            form.add_error('captcha', 'Неверная капча')
        else:
            # Поиск пользователя по email или телефону
            if login_input and password:
                try:
                    user_obj = User.objects.filter(email=login_input).first()
                    if not user_obj:
                        profile = UserProfile.objects.filter(phone=login_input).first()
                        if profile:
                            user_obj = profile.user
                    if user_obj:
                        user = authenticate(request, username=user_obj.username, password=password)
                except Exception:
                    user = None
            if not user:
                form.add_error(None, 'Неверный логин или пароль')
        # Генерируем новую капчу для следующей попытки
        captcha_text = generate_captcha_text()
        request.session['captcha_text'] = captcha_text
        captcha_image = generate_captcha_image(captcha_text)
        if user and captcha_input == captcha_session:
            login(request, user)
            request.session.pop('captcha_text', None)
            if user.username == 'admin':
                return redirect('admin_dashboard')
            return redirect('index')
        return render(request, 'main/login.html', {'form': form, 'captcha_image': captcha_image})
    else:
        form = LoginForm()
        captcha_text = generate_captcha_text()
        request.session['captcha_text'] = captcha_text
        captcha_image = generate_captcha_image(captcha_text)
    return render(request, 'main/login.html', {'form': form, 'captcha_image': captcha_image})

def logout_view(request):
    logout(request)
    return redirect('login')

def calculator_view(request):
    return render(request, 'main/calculator.html')

def catalog_view(request):
    products = Product.objects.all()
    return render(request, 'main/catalog.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    gallery = product.gallery.all()
    reviews = product.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'main/product_detail.html', {
        'product': product,
        'gallery': gallery,
        'reviews': reviews,
        'form': form,
    })

@login_required
def admin_dashboard(request):
    if request.user.username != 'admin':
        return redirect('index')
    return render(request, "main/admin_dashboard.html")

class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def captcha_refresh(request):
    captcha_text = generate_captcha_text()
    request.session['captcha_text'] = captcha_text
    captcha_image = generate_captcha_image(captcha_text)
    return JsonResponse({'captcha_image': captcha_image})

class UserListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class ReviewListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        reviews = Review.objects.select_related('product').all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

def cart_count(request):
    cart = request.session.get('cart', {})
    return JsonResponse({'cart_count': sum(cart.values())})

@login_required
def profile_view(request):
    profile = request.user.profile
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if 'delete_avatar' in request.POST:
            if profile.avatar:
                if os.path.isfile(profile.avatar.path):
                    os.remove(profile.avatar.path)
                profile.avatar = None
                profile.save()
            return redirect('profile')
        if form.is_valid():
            profile = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            profile.save()
            return redirect('profile')
    else:
        initial = {'email': user.email}
        form = ProfileForm(instance=profile, initial=initial)
    return render(request, 'main/profile.html', {'form': form, 'profile': profile})

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        return Response([{"id": c.id, "name": c.name} for c in categories])
