from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import CustomUser
from .utils import Util



""" Serialization for CustomUser Authentification """
class UserRegistrationSerializer(serializers.ModelSerializer):
  # Ro'yhatdan o'tish vaqtida parolni tekshirish uchun password2 maydoni yaratib olindi
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = CustomUser
    fields = (
            "password",
            "password2", 
            "first_name",
            "last_name",
            "email",
            "username",
            "passport",
            "date_of_bith",
            "phone1",
            "phone2",
            "gender",
            "address",
        )
    extra_kwargs={
      'password':{'write_only':True}
    }

  # parollarni validatsiyadan o'tkazish va bir biriga mosligini tekshirib chiqamiz
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Kiritilgan parollar birxil emas !!!")
    return attrs

  def create(self, validate_data):
    validate_data.pop('password2') 
    return CustomUser.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.Serializer):
    passport = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        passport = attrs.get('passport')
        password = attrs.get('password')

        # Foydalanuvchini passport va password orqali autentifikatsiya qilishi kerak
        user = authenticate(passport=passport, password=password)
        if not user:
            raise serializers.ValidationError("Passport yoki parol noto'g'ri !")
        attrs['user'] = user
        return attrs
      
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    # Tokenni blacklist ga qo'shish
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError("Tokenni blacklist ga qo'shib bo'lmadi, yoki bu token avval ishlatilgan !")
      

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    # Parollarni tekshirish
    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "Eski parol noto'g'ri !!"})
        return attrs
  

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Bu email bilan foydalanuvchi mavjud emas.")
        return attrs


class UserPasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Parollar bir xil bo'lishi kerak."})
        return attrs

      
  
      
      
      
      
      

    