from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, CartViewSet, UserViewSet


router = DefaultRouter()
# Product
router.register('products', ProductViewSet) 
                                #the endpoint is http://127.0.0.1:8000/shopapi/products/
# Order
router.register('order', OrderViewSet)
                                #the endpoint is http://127.0.0.1:8000/shopapi/order/
# Cart
router.register('cart', CartViewSet, basename='cart')

# user authentication
router.register('users', UserViewSet, basename='user')


urlpatterns = [

    path ('', include (router.urls)),
]