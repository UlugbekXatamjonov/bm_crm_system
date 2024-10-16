from django.db import models
from users.models import CustomUser
from group.models import Group
from worker.models import PERSONAL_STATUS


class Student(models.Model):
    """
    O'quvchi modeliga oid maydonlar.
    - user: Foydalanuvchi modeliga bog'langan.
    - group: O'quvchining guruhi.
    - is_discount: Chegirma borligi.
    - discount_amount: Chegirma miqdori.
    """
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sinf")
    is_discount = models.BooleanField(default=False, verbose_name="Chegirma")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Chegirma miqdori")
    personal_status = models.CharField(max_length=100, null=True, blank=True, choices=PERSONAL_STATUS, default="student", verbose_name="Shaxsiy status")
    
    def __str__(self):
        return self.user.get_full_name()

class Father_and_Mother(models.Model):
    """
    Ota-ona modeliga oid maydonlar.
    - user: Foydalanuvchi modeliga bog'langan.
    - mother_full_name: Onaning to'liq ismi.
    - mother_phone1, mother_phone2: Onaning telefon raqamlari.
    - children: Farzandlari.
    """
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    mother_full_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Onasining ismi")
    mother_phone1 = models.CharField(max_length=15, null=True, blank=True, verbose_name="Onasining tel 1- raqami")
    mother_phone2 = models.CharField(max_length=15, null=True, blank=True, verbose_name="Onasining tel 2- raqami")
    personal_status = models.CharField(max_length=100, null=True, blank=True, choices=PERSONAL_STATUS, default="father", verbose_name="Shaxsiy status")
    
    children = models.ManyToManyField(Student, related_name='parents', verbose_name="Bolalar")

    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    
