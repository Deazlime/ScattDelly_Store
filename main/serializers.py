from rest_framework import serializers
from .models import Product, Review, UserProfile
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    main_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = ['main_image_url']

    def get_main_image_url(self, obj):
        if obj.main_image and hasattr(obj.main_image, 'url'):
            return obj.main_image.url
        return None

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_active'] 