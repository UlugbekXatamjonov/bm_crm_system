from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.html import mark_safe


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, username,
                    passport, date_of_bith, phone1, phone2, gender, address,
                    password=None): 

        if not passport:
            raise ValueError("Foydalanuvchida 'passport' bo'lishi shart !")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email = email,
            username = username,
            passport = passport, 
            date_of_bith = date_of_bith,
            phone1 = phone1,
            phone2 = phone2,
            gender = gender,
            address = address
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):

        user = self.create_user(
            password=password,
            first_name='Admin',
            last_name='Admin',
            email = email,
            passport = "AA0000000", 
            date_of_bith = "01-01-2000",
            phone1 = '998990000000',
            phone2 = '998990000001',
            gender = "male",
            address = "Address"
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

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

