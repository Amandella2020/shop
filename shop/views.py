# from django.shortcuts import render
from .models import Product, Order
from  .serializers import ProductSerializer, OrderSerializer
from rest_framework import viewsets

# Create your views here.

class ProductViewSet (viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
