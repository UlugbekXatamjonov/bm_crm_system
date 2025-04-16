from django.db import models
import os

from users.models import CustomUser
from science.models import Science

from autoslug import AutoSlugField


""" Rasmlarni saqlash uchun fayl yo'laklarini user nomi bilan nomlash uchun funksiyalar """
def teacher_directory_path(instance, filename):
    # Foydalanuvchining to'liq ismini olish. Bo'shliqlarni va ' belgilarini olib tashlash
    teacher_name = instance.user.get_full_name().replace(" ", "_").replace("'","").lower()
    
    # Faylni saqlash yo'li
    return f'teachers/{teacher_name}_{instance.user.id}/personal_photo/{filename}'

def teacher_certificate_directory_path(instance, filename):
    # Foydalanuvchining to'liq ismini olish. Bo'shliqlarni va ' belgilarini olib tashlash
    teacher_name = instance.teacher_name.user.get_full_name().replace(" ", "_").replace("'","").lower()
    
    # Faylni saqlash yo'lini yaratish
    return f'teachers/{teacher_name}_{instance.teacher_name.user.id}/certificate_photo/{filename}'

def worker_directory_path(instance, filename):
    # Foydalanuvchining to'liq ismini olish. Bo'shliqlarni va ' belgilarini olib tashlash
    worker_name = instance.user.get_full_name().replace(" ", "_").lower()
    
    # Faylni saqlash yo'lini yaratish
    return f'workers/{worker_name}_{instance.user.id}/{filename}'



""" Teacherning slugi uchun funksiya """
""" Ikkita maydonni slugda birlashtirish """
def slug_funckion_for_teacher(self):
    """ O'qtuvchi uchun slugda uning ism va familiyasini birlashtirish uchun funksiya """        

    return "{}-{}".format(self.user.first_name, self.user.last_name)

def slug_funckion_for_teacher_certificate(self):
    """ O'qtuvchining sertifikati modelidagi  slug maydonida uning ismi familiyasi va sertifikat nomini birlashtiruvchi funksiya """
    
    return "{}-{}-{}".format(self.teacher_name.user.first_name, self.teacher_name.user.last_name, self.name)

def slug_funckion_for_teacher_social_media(self):
    """ O'qtuvchining Social Media modelidagi  slug maydonida uning ismi familiyasi va sertifikat nomini birlashtiruvchi funksiya """
    
    return "{}-{}-{}".format(self.teacher_name.user.first_name, self.teacher_name.user.last_name, self.name)



""" O'qtuvchi uchun modellar """
class Teacher(models.Model):
    """
    O'qituvchi modeliga oid maydonlar:
    - user: Foydalanuvchi modeliga bog'langan moydon.
    - slug: slug_funckion_for_teacher funksiyasi asosida olingan slug joylashgan maydon.
    - photo: O'qtuvchining rasmi.
    - passport_photo: O'qtuvchining passporti rasmi. 
    - science: O'qituvchining o'qitadigan fani.
    - dagree: O'qtuvchining ma'lumoti/darajasi.
    -experience: O'qtuvchining ish tajribasi.
    - is_class_leader: Sinf rahbari ekanligi.
    - is_mainpage: O'qtuvchi asosiy sahifadagi Teachers bo'limiga chiqish-chiqmasligi.
    - start_time: Ish boshlagan vaqti
    
    """
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    slug = AutoSlugField((u'slug'), populate_from=slug_funckion_for_teacher, unique=True)
    photo = models.ImageField(upload_to=teacher_directory_path, null=True, blank=True, verbose_name="Rasm")
    passport_photo = models.ImageField(upload_to=teacher_directory_path, null=True, blank=True, verbose_name="Passport rasmi")
    # salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")
    science = models.ForeignKey(Science, on_delete=models.CASCADE, related_name="teacher_science", verbose_name="Fan")
    dagree = models.CharField(max_length=50, verbose_name="Ma'lumoti", null=True, blank=True)
    experience = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tajriba(yilda)")
    start_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Ish boshlagan vaqti")
    
    
    is_class_leader = models.BooleanField(default=False, verbose_name="Sinf rahbar")
    is_mainpage = models.BooleanField(default=False, blank=True, null=True, verbose_name="Asosiy sahifa")
    
    # class_group = models.ForeignKey('group.Group', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.science}"


class Teacher_Certificate(models.Model):
    """ O'qtuvchining sertifikatlari uchun model.
        - teacher_name: Teacher modeliga ulangan.
        - name: Sertifikat nomi.
        - photo: Sertifikat rasmi.
    """
    
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_certificates', verbose_name="O'qtuvchi")
    name = models.CharField(max_length=250, verbose_name="Sertifikat nomi")
    slug = AutoSlugField(populate_from=slug_funckion_for_teacher_certificate, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to=teacher_certificate_directory_path, verbose_name="Rasmi")
    
    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        
    def __str__(self):
        return self.name


class Teacher_SocialMedia(models.Model):
    """ O'qtuvchining ijtimoiy tarmoqlari uchun model 
        - teacher_name: Teacher modeliga ulangan.
        - name: ijtimoiy tarmoq nomi.
        - url: ijtimoiy tarmoq manzili.
    """
    
    """ SM- Social Media - Ijtimoiy tarmoqlar """
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
    
    teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_sms', verbose_name="O'qtuvchi")
    name = models.CharField(max_length=50, choices=SM, verbose_name="Nomi")
    slug = AutoSlugField(populate_from=slug_funckion_for_teacher_social_media, unique=True, null=True, blank=True)
    url = models.CharField(max_length=250, verbose_name="URL")
   
   
   
""" -------  Xodimlar uchun modellar ------- """
class Worker(models.Model):
    """
    Maktab xodimi modeliga oid maydonlar.
    - user: Foydalanuvchi modeliga bog'langan.
    - position: Xodimning lavozimi.
    - is_superadmin: Superadmin ekanligini belgilash.
    """
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=worker_directory_path, null=True, blank=True, verbose_name="Rasm")
    # position = models.CharField(max_length=100, choices=WORKER_POSITION, default='worker', verbose_name="Lavozim")
    is_superadmin = models.BooleanField(default=False, verbose_name="Tizimga kirish huquqi")
    # salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")

    def __str__(self):
        return f"{self.user.get_full_name()}"






