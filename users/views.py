from django.contrib.auth import authenticate
from pprint import pprint

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets


from .renderers import UserRenderer
from .models import CustomUser

from .serializers import \
    UserRegistrationSerializer,\
        UserLoginSerializer,\
        LogoutSerializer,\
        UserChangePasswordSerializer,\
        SendPasswordResetEmailSerializer,\
        UserPasswordResetSerializer,\
        UserProfileSerializer



""" Viewsets for User Authentication """
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    # renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token': token, 'message': "Ro'yhatdan muvaffaqiyatli o'tdingiz"}, status=status.HTTP_201_CREATED)

from pprint import pprint

class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
             
        if serializer.is_valid():
            user = serializer.validated_data['user']

            """ Login bo'lgan userning ma'lumotlarini bazadan passporti bo'yicha olamiz  """
            active_user = CustomUser.objects.get(passport=serializer.data['passport'])
            active_user_serializer = UserProfileSerializer(active_user)
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user":active_user_serializer.data # userning shasiy ma'lumotlari
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tizimdan muvaffaqiyatli chiqdingiz !"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Parol muvaffaqiyatli o'zgartirildi"}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': "Parolni tiklash uchun link yuborildi. Iltimos emailingizni tekshiring"}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Parol muvaffaqiyatli yangilandi'}, status=status.HTTP_200_OK)






