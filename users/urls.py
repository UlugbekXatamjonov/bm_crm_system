from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from rest_framework.routers import DefaultRouter

from .views import (
    UserRegistrationView, \
    UserLoginView,\
    LogoutAPIView,\
    UserChangePasswordView,\
    SendPasswordResetEmailView,\
    UserPasswordResetView
)

app_name = 'student'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)), 
    
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    path('reset-password-email/', SendPasswordResetEmailView.as_view(), name='reset_password_email'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset_password'),
]


