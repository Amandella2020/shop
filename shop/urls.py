from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet

router = DefaultRouter()

router.register('products', ProductViewSet) 
                                #the endpoint is http://127.0.0.1:8000/shopapi/products/
router.register('order', OrderViewSet)
                                #the endpoint is http://127.0.0.1:8000/shopapi/order/
urlpatterns = [

    path ('', include (router.urls)),
]