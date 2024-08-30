from django.db import models
from worker.models import Teacher


class Group(models.Model):
    """
    Guruh modeliga oid maydonlar.
    - class_name: Sinf nomi.
    - teacher: O'qituvchi bilan bog'langan.
    """
    
    class_name = models.CharField(max_length=30, verbose_name="Sinf nomi")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Sinf rahbar")

    def __str__(self):
        return self.class_name
    
    
