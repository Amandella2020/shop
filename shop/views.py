# from django.shortcuts import render
from .models import Product, Order, Cart, CartItem
from  .serializers import ProductSerializer, OrderSerializer, CartItemSerializer, CartSerializer, AddToCartSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from django.contrib.auth.models import User
import random
import uuid
from django.shortcuts import get_object_or_404




# Create your views here.

class ProductViewSet (viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] 
    authentication_classes = []  

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]



    # Mock payment endpoint 
    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        

        #Prevents paying twice
        if order.payment_status == 'paid':
            return Response(
                {"message": "Order already paid"},
                status=status.HTTP_400_BAD_REQUEST
            )


        # Simulate payment (random success/failure)
        success = True   

        if success:
            order.payment_status = 'paid'
            order.save()

            return Response({
                "message": "Payment successful",
                "order_id": order.id,
                "amount": order.total_price,
                 "payment_ref": str(uuid.uuid4()),   # fake transaction ID
                "status": "paid"
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Payment failed ❌",
            "order_id": order.id,
            "amount": order.total_price,
            "status": "pending"
        }, status=status.HTTP_400_BAD_REQUEST)

# shopping cart

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # view current user's cart
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # POST /cart/add/ → add item to cart
    @action(detail=False, methods=['post'])
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()
        return Response({
    "message": "Item added to cart",
    "data": CartItemSerializer(cart_item).data
}, status=status.HTTP_201_CREATED)

    # PATCH /cart/update/<cart_item_id>/ → update quantity
    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cart_item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETE /cart/remove/<cart_item_id>/ → remove item
    @action(detail=True, methods=['delete'])
    def remove(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in your cart"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({"success": "Item removed"}, status=status.HTTP_204_NO_CONTENT)

# user authentication (JWT)

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # GET /users/<id>/
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    # GET /users/
    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # POST /users/
    def create(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    # PATCH /users/<id>/
    def partial_update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT/users/<id>/
    def update(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /users/<id>/
    def destroy(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
