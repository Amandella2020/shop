from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404
from .models import Product,Order, Cart, CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:        
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'total_price']


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CartItem
        fields  = ['id', 'product', 'product_name', 'quantity', 'total_price']
        read_only_fields = ['total_price']



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at']


# Add-to-cart logic
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)

    def save(self, **kwargs):
        user = self.context['request'].user
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        product = get_object_or_404(Product, id=product_id)

        # Get or create cart
        cart, created =Cart.objects.get_or_create(user=user)

        # Check if item already exists
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            # If already exists → increase quantity
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()

        return cart_item


# user authentication (JWT)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

# customizing user authentication (JWT)
class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add extra info inside token
        token['username'] = user.username

        return token