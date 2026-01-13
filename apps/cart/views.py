from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from .models import Cart, CartItem, UserCourse
from .serializers import CartSerializer, CartItemSerializer, AddToCartSerializer
from ..courses.models import Course


class CartViewSet(viewsets.GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()

    def get_cart(self, request: object) -> tuple[Cart, bool]:
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def list(self, request, *args, **kwargs):
        cart = self.get_cart(request)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        course_id = serializer.validated_data['course_id']
        course = Course.objects.get(id=course_id)
        cart = self.get_cart(request)
        cart, created = CartItem.objects.get_or_create(cart=cart,course=course)

        if created:
            return Response(
                {"detail": "Course added to basket."},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"detail": "Курс уже в корзине"},
                status=status.HTTP_200_OK
            )

    @action(detail=False, methods=['delete'], url_path='remove/(?P<course_id>[^/.]+)')
    def remove(self, request, course_id=None):
        cart = self.get_cart(request)

        cart_item = CartItem.objects.get(cart=cart,course_id=course_id)
        cart_item.delete()
        return Response(
            {"detail": "Course removed from basket."},
            status=status.HTTP_204_NO_CONTENT
        )


    @action(detail=False, methods=['delete'])
    def clear(self, request):
        cart = self.get_cart(request)

        cart.items.all().delete()
        return Response(
            {"detail": "Basket cleared."},
            status=status.HTTP_204_NO_CONTENT
        )

