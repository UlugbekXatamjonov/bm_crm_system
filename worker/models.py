from django.db import models
from users.models import CustomUser
import os

def teacher_directory_path(instance, filename):
    # Foydalanuvchining to'liq ismini olamiz
    teacher_name = instance.user.get_full_name().replace(" ", "_").lower()
    
    # Faylni saqlash yo'lini yaratamiz
    return f'teachers_photos/{teacher_name}_{instance.user.id}/{filename}'

def worker_directory_path(instance, filename):
    # Foydalanuvchining to'liq ismini olamiz
    worker_name = instance.user.get_full_name().replace(" ", "_").lower()
    
    # Faylni saqlash yo'lini yaratamiz
    return f'workers_photos/{worker_name}_{instance.user.id}/{filename}'

PERSONAL_STATUS = [
        ('teacher',"O'qtuvchi"),
        ('asistent_teacher',"Asistent o'qtuvchi"),
        ('father',"Ota-ona"),
        ('student',"O'quvchi"),
    ]
    

class Teacher(models.Model):
    """
    O'qituvchi modeliga oid maydonlar.
    - user: Foydalanuvchi modeliga bog'langan.
    - salary: O'qituvchining maoshi.
    - subject: O'qituvchining o'qitadigan fani.
    - is_class_leader: Sinf rahbari ekanligi.
    - class_group: Sinf guruhi bilan bog'langan.
    """
    
    TEACHER_SUBJECTS = [
        ('math','Matematika'),
        ('ict','Informatika'),
        ('english','Ingliz tili'),
        ('russian','Rus tili'),
        ('mather_language','Ona tili'),
        ('history','Tarix'),
        ('sat','SAT'),
        ('pe','Jismoniy tarbiya'),
        ('geography','Geografiya'),
        ('mental','Mental arifmetika'),
        ('biology','Biologiya'),
        ('chemistry','Kimyo'), 
    ]
    
    TEACHER_PERSONAL_STATUS = [
        ('teacher',"O'qtuvchi"),
        ('asistent_teacher',"Asistent o'qtuvchi")
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=teacher_directory_path, null=True, blank=True, verbose_name="Rasm")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")
    subject = models.CharField(max_length=100, choices=TEACHER_SUBJECTS, null=True, blank=True, verbose_name="Fan")
    is_class_leader = models.BooleanField(default=False, verbose_name="Sinf rahbar")
    # class_group = models.ForeignKey('group.Group', on_delete=models.SET_NULL, null=True)
    personal_status = models.CharField(max_length=100, null=True, blank=True, choices=PERSONAL_STATUS, default="teacher", verbose_name="Shaxsiy status")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.subject}"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.subject}"


class Worker(models.Model):
    """
    Maktab xodimi modeliga oid maydonlar.
    - user: Foydalanuvchi modeliga bog'langan.
    - position: Xodimning lavozimi.
    - is_superadmin: Superadmin ekanligini belgilash.
    - salary: Xodimning maoshi.
    """
    
    WORKER_POSITION = [
        ("manager", "Direktor"),
        ("little_manager", "Mudir"),
        ("assistant", "Kotiba"),
        ("worker", "Oddiy hodim"),
        
        # ("director", "Direktor"),
        # ("cook", "Oshpaz"),
        # ("kitchen_staff", "Oshxona hodimi"),
        # ("cleaner", "Tozalovchi"),
        # ("guard", "Qorovul"),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=worker_directory_path, null=True, blank=True, verbose_name="Rasm")
    position = models.CharField(max_length=100, choices=WORKER_POSITION, default='worker', verbose_name="Lavozim")
    is_superadmin = models.BooleanField(default=False, verbose_name="Tizimga kirish huquqi")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


