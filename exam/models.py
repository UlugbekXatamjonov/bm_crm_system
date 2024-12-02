from django.db import models

# Create your models here.



class Weeky_exam_photos(models.Model):
    """ Haftalik imtihonlardan olingan rasmlar  uchun model """
    
    photo = models.ImageField(upload_to="weekly_exam_photos", verbose_name="")
    status = models.BooleanField(default=True, verbose_name="Holati")
    created_on = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Imtihon"
        verbose_name_plural = "Imtihonlar"
    
    def __str__(self):
        return f"{self.id} photo"
    
    
    