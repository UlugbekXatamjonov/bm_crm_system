from django.urls import path, include

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView


app_name = 'student'

router = DefaultRouter()

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="registration"),

    path('', include(router.urls))
]




