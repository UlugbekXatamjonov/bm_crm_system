from django.db import models

from users.models import CustomUser

from autoslug import AutoSlugField

# Create your models here.

class Science(models.Model):
    """ Fanlar uchun model """
    name = models.CharField(max_length=250, verbose_name="Fan nomi")
    slug = AutoSlugField(populate_from='name', unique=True)
    photo = models.ImageField(upload_to='science_photos/', verbose_name="Rasm")
    about = models.TextField(blank=True, null=True, verbose_name="Fan haqida")
    
    
    is_mainpage = models.BooleanField(default=False, blank=True, null=True, verbose_name="Asosiy sahifa")
    status = models.BooleanField(default=True, verbose_name="Holati")
    
    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"
    
    def __str__(self):
        return self.name