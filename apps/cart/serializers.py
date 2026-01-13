from rest_framework import serializers
from .models import Cart, CartItem
from apps.courses.serializers import CourseSerializer


class CartItemSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many= True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class AddToCartSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

