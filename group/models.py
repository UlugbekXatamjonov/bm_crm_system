from django.db import models

from autoslug import AutoSlugField

from worker.models import Teacher


class Group(models.Model):
    """
    Guruh modeliga oid maydonlar.
    - class_name: Sinf nomi.
    - teacher: O'qituvchi bilan bog'langan.
    """
    
    class_name = models.CharField(max_length=30, verbose_name="Sinf nomi")
    slug = AutoSlugField(populate_from='class_name', unique=True, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher_group', verbose_name="Sinf rahbar")

    class Meta:
        verbose_name = "Sinf"
        verbose_name_plural = "Sinflar"

    def __str__(self):
        return self.class_name
    
    
