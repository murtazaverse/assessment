from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Order
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            refresh = RefreshToken.for_user(user)
            data['token'] = str(refresh.access_token)
        else:
            raise serializers.ValidationError("Invalid login credentials")
        return data