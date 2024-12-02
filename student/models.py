from django.db import models

from users.models import CustomUser
from group.models import Group
from science.models import Science


""" Rasmlarni saqlash uchun fayl yo'laklarini user nomi bilan nomlash uchun funksiyalar """

def student_certificate_directory_path(instance, filename):
    # O'quvchining to'liq ismini olish. Bo'shliqlarni va ' belgilarini olib tashlash
    student_name = instance.student.user.get_full_name().replace(" ", "_").replace("'","").lower()
    
    # Faylni saqlash yo'lini yaratish
    return f'students/{student_name}_{instance.student.user.id}/certificate_photo/{filename}'

def student_photo_directory_path(instance, filename):
    # O'quvchining to'liq ismini olish. Bo'shliqlarni va ' belgilarini olib tashlash
    student_name = instance.user.get_full_name().replace(" ", "_").replace("'","").lower()
    
    # Faylni saqlash yo'lini yaratish
    return f'students/{student_name}_{instance.user.id}/photo/{filename}'



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
    photo = models.ImageField(upload_to=student_photo_directory_path, null=True, blank=True, verbose_name="Rasm")

    is_discount = models.BooleanField(default=False, verbose_name="Chegirma")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Chegirma miqdori")
    # personal_status = models.CharField(max_length=100, null=True, blank=True, choices=PERSONAL_STATUS, default="student", verbose_name="Shaxsiy status")
    
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
    # personal_status = models.CharField(max_length=100, null=True, blank=True, choices=PERSONAL_STATUS, default="father", verbose_name="Shaxsiy status")
    
    children = models.ManyToManyField(Student, related_name='parents', verbose_name="Bolalar")

    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    
class Student_Certificate(models.Model):
    """ O'quvchilarning natijalari va Sertifikatlari uchun model """
    
    student  = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_result', verbose_name="O'quvchi")
    science = models.ForeignKey(Science, on_delete=models.CASCADE, related_name="students", verbose_name="Fan")
    name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Sertifikat nomi")
    photo = models.ImageField(upload_to=student_certificate_directory_path, verbose_name="Rasm")
    about = models.TextField(verbose_name="Batafsil")
    is_mainpage = models.BooleanField(verbose_name="Asosiy sahifa")
    
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.first_name} - {self.name}"
    

