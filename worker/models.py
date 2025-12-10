from django.db import models
import os

from users.models import CustomUser
from science.models import Science

from autoslug import AutoSlugField
from django.utils import timezone
from django.utils.text import slugify





def teacher_photo_path(instance, filename):
    """ O'qituvchi rasmi saqlanadigan dinamik papka yo'li."""
    
    return f"teachers/{instance.user.id}_{instance.user.first_name}_{instance.user.last_name}/photos/{filename}"


def teacher_passport_path(instance, filename):
    """ Pasport rasmlar uchun alohida papka."""
    
    return f"teachers/{instance.user.id}_{instance.user.first_name}_{instance.user.last_name}/passport/{filename}"


def unique_slug_generator(instance):
    """ Teacher uchun unik(slug) yaratadigan funksiya. Takror bo'lsa: name-1, name-2 ko'rinishda davom etadi. """
    
    base_slug = slugify(f"{instance.user.first_name}-{instance.user.last_name}")
    slug = base_slug
    counter = 1

    Model = instance.__class__

    while Model.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug


class Teacher(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Avtomatik generatsiya qilinadi.")

    photo = models.ImageField(upload_to=teacher_photo_path, blank=True, null=True)
    passport_photo = models.ImageField(upload_to=teacher_passport_path, blank=True, null=True)

    science = models.ForeignKey(Science, on_delete=models.CASCADE, related_name="teachers")
    dagree = models.CharField(max_length=100, blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)

    start_time = models.DateField(default=timezone.now)
    is_class_leader = models.BooleanField(default=False)
    is_mainpage = models.BooleanField(default=False)

    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """
        Slug avtomatik generatsiya.
        Faqat yangi yaratilganda ishlaydi.
        """
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Teacher: {self.user.first_name} {self.user.last_name}"


def teacher_certificate_path(instance, filename):
    """ Sertifikat rasmini saqlash uchun dinamik path. """

    teacher = instance.teacher
    return f"teachers/{teacher.user.id}_{teacher.user.first_name}_{teacher.user.last_name}/certificates/{filename}"


class Teacher_Certificate(models.Model):
    """ O'qituvchining sertifikatlari uchun model. """

    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, related_name="teacher_certificates", help_text="Qaysi o'qituvchiga tegishli sertifikat.")
    name = models.CharField(max_length=250, help_text="Sertifikat nomi.")

    slug = models.SlugField(max_length=260, unique=True, blank=True, null=True, help_text="SEO uchun avtomatik yaratiladigan slug.")
    photo = models.ImageField(upload_to=teacher_certificate_path, help_text="Sertifikatning rasmi.")
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sertifikat"
        verbose_name_plural = "Sertifikatlar"
        ordering = ["-id"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["name"]),
        ]

    def save(self, *args, **kwargs):
        """Slug avtomatik generatsiya bo'lishi"""
        
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.teacher.user.first_name})"


class SocialMediaChoices(models.TextChoices):
    TELEGRAM1 = "telegram1", "Telegram 1"
    TELEGRAM2 = "telegram2", "Telegram 2"
    INSTAGRAM = "instagram", "Instagram"
    FACEBOOK  = "facebook",  "Facebook"
    YOUTUBE   = "youtube",   "YouTube"
    LINKEDIN  = "linkedin",  "LinkedIn"
    BLOG1     = "blog1",     "Blog 1"
    BLOG2     = "blog2",     "Blog 2"


class Teacher_SocialMedia(models.Model):
    """ O'qituvchining ijtimoiy tarmoqlari uchun model. """

    teacher = models.ForeignKey("Teacher", on_delete=models.CASCADE, related_name="teacher_sms", help_text="O'qituvchining qaysi ijtimoiy tarmog'i.")
    name = models.CharField(max_length=50, choices=SocialMediaChoices.choices, help_text="Ijtimoiy tarmoq nomi.")

    slug = models.SlugField(max_length=260, unique=True, blank=True, null=True, help_text="Tarmoq uchun slug (SEO uchun).")
    url = models.URLField(max_length=300, help_text="Ijtimoiy tarmoq manzili (URL).")
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Ijtimoiy tarmoq"
        verbose_name_plural = "Ijtimoiy tarmoqlar"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        """Slug avtomatik generatsiya qilinadi"""
        
        if not self.slug:
            self.slug = slugify(f"{self.teacher.id}-{self.name}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher.user.first_name} - {self.get_name_display()}"



# -----------------------------------   ❗ ESKI KODLAR ❗ --------------------------------------------  #



# """ Rasmlarni saqlash uchun fayl yo'laklarini user nomi bilan nomlash uchun funksiyalar """
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



# """ Teacherning slugi uchun funksiya """
# """ Ikkita maydonni slugda birlashtirish """
def slug_funckion_for_teacher(self):
    """ O'qtuvchi uchun slugda uning ism va familiyasini birlashtirish uchun funksiya """        

    return "{}-{}".format(self.user.first_name, self.user.last_name)

def slug_funckion_for_teacher_certificate(self):
    """ O'qtuvchining sertifikati modelidagi  slug maydonida uning ismi familiyasi va sertifikat nomini birlashtiruvchi funksiya """
    
    return "{}-{}-{}".format(self.teacher_name.user.first_name, self.teacher_name.user.last_name, self.name)

def slug_funckion_for_teacher_social_media(self):
    """ O'qtuvchining Social Media modelidagi  slug maydonida uning ismi familiyasi va sertifikat nomini birlashtiruvchi funksiya """
    
    return "{}-{}-{}".format(self.teacher_name.user.first_name, self.teacher_name.user.last_name, self.name)



# """ O'qtuvchi uchun modellar """
# class Teacher(models.Model):
#     """
#     O'qituvchi modeliga oid maydonlar:
#     - user: Foydalanuvchi modeliga bog'langan moydon.
#     - slug: slug_funckion_for_teacher funksiyasi asosida olingan slug joylashgan maydon.
#     - photo: O'qtuvchining rasmi.
#     - passport_photo: O'qtuvchining passporti rasmi. 
#     - science: O'qituvchining o'qitadigan fani.
#     - dagree: O'qtuvchining ma'lumoti/darajasi.
#     -experience: O'qtuvchining ish tajribasi.
#     - is_class_leader: Sinf rahbari ekanligi.
#     - is_mainpage: O'qtuvchi asosiy sahifadagi Teachers bo'limiga chiqish-chiqmasligi.
#     - start_time: Ish boshlagan vaqti
    
#     """
    
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     slug = AutoSlugField((u'slug'), populate_from=slug_funckion_for_teacher, unique=True)
#     photo = models.ImageField(upload_to=teacher_directory_path, null=True, blank=True, verbose_name="Rasm")
#     passport_photo = models.ImageField(upload_to=teacher_directory_path, null=True, blank=True, verbose_name="Passport rasmi")
#     # salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maosh")
#     science = models.ForeignKey(Science, on_delete=models.CASCADE, related_name="teacher_science", verbose_name="Fan")
#     dagree = models.CharField(max_length=50, verbose_name="Ma'lumoti", null=True, blank=True)
#     experience = models.CharField(max_length=50, null=True, blank=True, verbose_name="Tajriba(yilda)")
#     start_time = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Ish boshlagan vaqti")
    
    
#     is_class_leader = models.BooleanField(default=False, verbose_name="Sinf rahbar")
#     is_mainpage = models.BooleanField(default=False, blank=True, null=True, verbose_name="Asosiy sahifa")
    
#     # class_group = models.ForeignKey('group.Group', on_delete=models.SET_NULL, null=True)
    
#     def __str__(self):
#         return f"{self.user.get_full_name()} - {self.science}"


    



# class Teacher_Certificate(models.Model):
#     """ O'qtuvchining sertifikatlari uchun model.
#         - teacher_name: Teacher modeliga ulangan.
#         - name: Sertifikat nomi.
#         - photo: Sertifikat rasmi.
#     """
    
#     teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_certificates', verbose_name="O'qtuvchi")
#     name = models.CharField(max_length=250, verbose_name="Sertifikat nomi")
#     slug = AutoSlugField(populate_from=slug_funckion_for_teacher_certificate, unique=True, null=True, blank=True)
#     photo = models.ImageField(upload_to=teacher_certificate_directory_path, verbose_name="Rasmi")
    
#     class Meta:
#         verbose_name = "Sertifikat"
#         verbose_name_plural = "Sertifikatlar"
        
#     def __str__(self):
#         return self.name


# class Teacher_SocialMedia(models.Model):
#     """ O'qtuvchining ijtimoiy tarmoqlari uchun model 
#         - teacher_name: Teacher modeliga ulangan.
#         - name: ijtimoiy tarmoq nomi.
#         - url: ijtimoiy tarmoq manzili.
#     """
    
#     """ SM- Social Media - Ijtimoiy tarmoqlar """
#     SM = (
#         ('telegram1',"Telegram 1"),
#         ('telegram2',"Telegram 2"),
#         ('twitter','Twitter'),
#         ('instagram','Instagram'),
#         ('facebook','Facebook'),
#         ('youtube','You Tube'),
#         ('linkedin','LinkedIn'),
#         ('blog1','Blog 1'),
#         ('blog2','Blog 2'),
#     )
    
#     teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_sms', verbose_name="O'qtuvchi")
#     name = models.CharField(max_length=50, choices=SM, verbose_name="Nomi")
#     slug = AutoSlugField(populate_from=slug_funckion_for_teacher_social_media, unique=True, null=True, blank=True)
#     url = models.CharField(max_length=250, verbose_name="URL")
   
   
   
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






