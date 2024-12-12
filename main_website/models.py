from django.db import models

from autoslug import AutoSlugField

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

