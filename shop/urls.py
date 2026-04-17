from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ProductViewSet, OrderViewSet, CartViewSet, UserViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
router.register('cart', CartViewSet, basename='cart')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]