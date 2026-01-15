from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(read_only=True, source='course.title')

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'course', 'course_title', 'amount',
                  'currency', 'status', 'created_at', 'paid_at']
        read_only_fields = ['order_id', 'amount', 'status', 'paid_at']