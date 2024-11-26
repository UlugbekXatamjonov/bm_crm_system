from django.db import models
import os

from users.models import CustomUser

from autoslug import AutoSlugField


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

def slug_funckion_for_teacher(self):
        """ Ikkita maydonni sludada birlashtirish """
        return "{}-{}".format(self.user.first_name, self.user.last_name)


""" -------  O'qtuvchi uchun modellar ------- """
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
    slug = AutoSlugField((u'slug'), populate_from=slug_funckion_for_teacher, unique=True)
    photo = models.ImageField(upload_to=teacher_directory_path, null=True, blank=True, verbose_name="Rasm")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")
    subject = models.CharField(max_length=100, choices=TEACHER_SUBJECTS, null=True, blank=True, verbose_name="Fan")
    dagree = models.CharField(max_length=50, verbose_name="Ma'lumoti", null=True, blank=True)
    experience = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tajriba(yilda)")
    
    is_class_leader = models.BooleanField(default=False, verbose_name="Sinf rahbar")
    is_mainpage = models.BooleanField(default=False, blank=True, null=True, verbose_name="Asosiy sahifa")
    
    
    
    # class_group = models.ForeignKey('group.Group', on_delete=models.SET_NULL, null=True)
    # personal_status = models.CharField(max_length=100, null=True, blank=True, choices=PERSONAL_STATUS, default="teacher", verbose_name="Shaxsiy status")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.subject}"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.subject}"


class Teacher_Certificate(models.Model):
    """ Sertifikatlar uchun model """
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_certificate', verbose_name="O'qtuvchi")
    name = models.CharField(max_length=250, verbose_name="Sertifikat nomi")
    
    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        
    def __str__(self):
        return self.name


class Teacher_SocialMedia(models.Model):
    """ Ijtimoiy tarmoqlar uchun model """
    SM = (
        ('telegram1',"Telegram 1"),
        ('telegram2',"Telegram 2"),
        ('twitter','Twitter'),
        ('instagram','Instagram'),
        ('facebook','Facebook'),
        ('youtube','You Tube'),
        ('linkedin','LinkedIn'),
        ('blog1','Blog 1'),
        ('blog2','Blog 2'),
    )
    
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_sm', verbose_name="O'qtuvchi")
    name = models.CharField(max_length=50, choices=SM, verbose_name="Nomi")
    url = models.CharField(max_length=250, verbose_name="URL")
   
   
""" -------  Xodimlar uchun modellar ------- """
class Worker(models.Model):
    """
    Maktab xodimi modeliga oid maydonlar.
    - user: Foydalanuvchi modeliga bog'langan.
    - position: Xodimning lavozimi.
    - is_superadmin: Superadmin ekanligini belgilash.
    - salary: Xodimning maoshi.
    """
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=worker_directory_path, null=True, blank=True, verbose_name="Rasm")
    # position = models.CharField(max_length=100, choices=WORKER_POSITION, default='worker', verbose_name="Lavozim")
    is_superadmin = models.BooleanField(default=False, verbose_name="Tizimga kirish huquqi")
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"


