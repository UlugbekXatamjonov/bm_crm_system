from django.db import models
from django.utils.timezone import datetime

from student.models import Student
from worker.models import Teacher, Worker

class Attendance(models.Model):
    """
    Davomat modeliga oid maydonlar.
    - student: Talaba bilan bog'langan.
    - teacher: O'qituvchi bilan bog'langan.
    - worker: Xodim bilan bog'langan.
    - date: Davomat sanasi.
    - came: Kelganligi.
    - comment: Izoh.
    """
    
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="O'quvchi")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="O'qtuvchi")
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Hodim")
    
    
    date = models.DateField(default=datetime.today, null=True, verbose_name="Sana")
    came = models.BooleanField(default=False, verbose_name="Kelmadi")
    comment = models.TextField(null=True, blank=True, verbose_name="Izoh")

    created_on = models.DateTimeField(auto_now_add=True, verbose_name="Davomat olingan sana")
    
    def __str__(self):
        return f"{self.student or self.teacher or self.worker} - {self.date}"


