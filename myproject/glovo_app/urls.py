from django.urls import path, include
from .views import (UserProfileListAPIView,UserProfileDetailAPIView,CategoryListAPIView,
                    CategoryDetailAPIView,StoreListAPIView,StoreDetailAPIView,ProductViewSet,
                    OrderViewSet,CourierViewSet,ReviewCreateAPIView,ReviewEditAPIView,
                    OrderStatusDetailAPIView,OrderStatusListAPIView,StoreViewSet,RegisterView,
                    CustomLoginView,LogoutView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)
from rest_framework.routers import SimpleRouter
from rest_framework import routers

router = SimpleRouter()
router.register('store_create', StoreViewSet)
router.register('product', ProductViewSet)
router.register('order', OrderViewSet)
router.register('courier', CourierViewSet)






urlpatterns = [
    path('', include(router.urls)),
    path('user/',UserProfileListAPIView.as_view(),name='user-list'),
    path('user/<int:pk>/',UserProfileDetailAPIView.as_view(),name='user-detail'),
    path('category/',CategoryListAPIView.as_view(),name='category-list'),
    path('category/<int:pk>/',CategoryDetailAPIView.as_view(),name='category-detail'),
    path('store/',StoreListAPIView.as_view(),name='store-list'),
    path('store/<int:pk>/',StoreDetailAPIView.as_view(),name='store-detail'),
    path('review/create/',ReviewCreateAPIView.as_view(),name='review-create'),
    path('review/create/<int:pk>/',ReviewEditAPIView.as_view(),name='review-edit'),
    path('order_status/',OrderStatusListAPIView.as_view(),name='order-list'),
    path('order_status/<int:pk>/',OrderStatusDetailAPIView.as_view(),name='order-detail'),


    path('register/', RegisterView.as_view(), name='register_list'),
    path('login/', CustomLoginView.as_view(), name='login_list'),
    path('logout/', LogoutView.as_view(), name='logout_list'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]