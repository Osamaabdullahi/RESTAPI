from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product,OrderedItem
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['admin'] = user.is_staff

        return token

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields="__all__"

        # fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class ProductSerilizer(serializers.ModelSerializer):
    class Meta:
        fields="__all__"
        model=Product


class OrderedItemSerilizer(serializers.ModelSerializer):
    # user=serializers.ReadOnlyField(source='user.first_name')
    # product=serializers.ReadOnlyField(source="product.name")
    class Meta:
        fields=["id","user","product","quantity","total_price","status"]
        model=OrderedItem


class OrderSerlizer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.first_name')
    product=serializers.ReadOnlyField(source="product.name")
    class Meta:
        fields=["id","user","product","quantity","total_price","status"]
        model=OrderedItem
