from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_confirm', 'first_name', 'last_name'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'The password field did not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),username=email,password=password)
            if not User:
                serializers.ValidationError("User not found.")
            if not user.is_active:
                serializers.ValidationError("The user account has been disabled.")
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "'Email' and 'password' must be included."
            )
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (   'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'avatar', 'bio', 'created_at', 'updated_at')
        read_only_fields = ('id', 'email', 'created_at', 'updated_at')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'avatar', 'bio', 'first_name', 'last_name'
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items:
            setattr(instance, attr, value)

