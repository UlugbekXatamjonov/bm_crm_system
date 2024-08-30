from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Foydalanuvchi modeliga qo'shimcha maydonlar qo'shildi.
    - passport: Foydalanuvchining pasport/tug'ilganlik haqida guvohnoma raqami.
    - date_of_bith: Tug'ilgan sanasi.
    - phone1, phone2: Aloqa telefon raqamlari (validator bilan tekshirilgan).
    - gender: Foydalanuvchining jinsi Erkak/Ayol (tanlov bilan).
    - address: Foydalanuvchining manzili.
    - status: Foydalanuvchi statusi (aktiv yoki yo'q).
    - created_at, updated_at: Ro'yxatga olish va yangilanish vaqti. 
    """
    
    phone_regex = RegexValidator(regex=r'^\+998\d{9}$', message="Telefon raqami '+998991234567' formatida kiritilishi kerak.")
    GENDER = [
        ('male', 'Erkak'), 
        ('female', 'Ayol')
    ]
    
    passport = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="Passport")
    date_of_bith = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    phone1 = models.CharField(validators=[phone_regex], max_length=13, null=True, blank=True, verbose_name="Telefon raqam")
    phone2 = models.CharField(validators=[phone_regex], max_length=13, null=True, blank=True, verbose_name="Telefon raqam")
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True, verbose_name="Jinsi")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Manzil")
    
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

