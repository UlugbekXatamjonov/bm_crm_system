from django.db import models

from autoslug import AutoSlugField # type: ignore

# Create your models here.


class Announcement(models.Model): # Announcement - E'lon
    """  E'lonlar bo'limi uchun model 
    name - E'lon nomi
    photo - E'lon rasmi
    about - E'lon haqida ma'lumot
    status - holati
    created_on - chop qilingan vaqti
    """

    name = models.CharField(max_length=250, verbose_name="E'lon nomi")
    slug = AutoSlugField(populate_from='name', unique=True)
    photo = models.ImageField(upload_to="announcement_photos/%Y/%m/", verbose_name="Rasmi")
    about = models.TextField(verbose_name="E'lon haqida")
    
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_on = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"

    def __str__(self):
        return self.name



class Parents_opinion(models.Model):
    """ Ota-onalar fikri """
    
    name = models.CharField(max_length=250, verbose_name="Ismi")
    opinion = models.TextField(verbose_name="Fikr")
    photo = models.ImageField(upload_to='parents_opinion/', 
                              default='D:/projects/my_projects/bm_crm_system/media/default_pictures/person.png', 
                              verbose_name="Rasm", null=True, blank=True)
    
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Ota-onalar fikri"
        verbose_name_plural = "Ota-onalar fikrlari"
    
    def __str__(self):
        return self.name
    
    

class Contact_us(models.Model):
    """ Biz bilan bog'laning sahifasi uchun model """

    name = models.CharField(max_length=250, verbose_name="Ismi")
    phone = models.CharField(max_length=50, verbose_name="Telefon raqam")
    
    status = models.BooleanField(default=False, verbose_name="Holati")
    created_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = "Xabar"
        verbose_name_plural = "Xabarlar"


    def __str__(self):
        return self.name
    
    
    

