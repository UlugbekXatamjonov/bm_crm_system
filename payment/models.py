from django.db import models
from django.utils import timezone
from student.models import Student

from config.project_veriables import PAYMENT_AMOUNT, MONTHS

class Payment(models.Model):
    """
    To'lov modeliga oid maydonlar.
    - payment_type: Daromad turi.
    - student: Talabaga bog'langan.
    - month: To'lov oyi.
    - year: To'lov yili.
    - amount_due: To'lov miqdori.
    - paid_amount: To'lov qilingan summa.
    - remaining_amount: Qoldiq to'lov miqdori (hisoblanadi).
    - payment_status: To'lov statusi (To'lanmagan, Yakunlanmagan, To'langan).
    - created_at: To'lovning yaratilgan vaqti.
    """
    
    PAYMENT_TYPE = [
        ("student_payment","Oylik to'lov"),
        ("other_income","Boshqa daromad"),
    ]
    
    PAYMENT_STATUS = [
        ("unpaid","To'lanmagan"),
        ("unfinished","Yakunlanmagan"),
        ("paid","To'langan"),
    ]
    
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, default="student_payment", verbose_name="Daromad turi")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, verbose_name="O'quvchi")
    month = models.CharField(max_length=20, choices=MONTHS, verbose_name="Oy")
    year = models.IntegerField(default=timezone.now().year, verbose_name="Yil")
    
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=PAYMENT_AMOUNT, null=True, blank=True, verbose_name="To'lov qilinishi kerak bo'lgan summa")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=PAYMENT_AMOUNT, verbose_name="To'langan summa")
    payment_status = models.CharField(max_length=30, choices=PAYMENT_STATUS, null=True, blank=True, verbose_name="To'lov holati")
    created_on = models.DateTimeField(auto_now_add=True)
        
    @property
    def remaining_amount(self):
        return self.amount_due - self.paid_amount - (self.student.discount_amount or 0)

    def __str__(self):
        return f"{self.student} - {self.year} {self.month}"


class Expenses(models.Model):
    """
    Xarajatlar modeliga oid maydonlar.
    - expenses_type: Xarajat turi.
    - title: Xarajat nomi.
    - amount: Xarajat miqdori.
    - comment: Izoh.
    """
    
    EXPENSES_TYPES = [
        ("utility_bills","Komunal to'lovlar"),
        ("monthly salaries","Maoshlar"),
        ("foods","Oziq ovqat"),
        ("construction","Tamirlash va qurilish"),
        ("educational_tools","Kanstovar"),
        ("construction","Qurilish"),
        ("furniture","Mebellar"),
        # ("",""),
    ]
    
    expenses_type = models.CharField(max_length=30, choices=EXPENSES_TYPES, verbose_name="Xarajat turi")
    title = models.CharField(max_length=250, verbose_name="Nomi")
    month = models.CharField(max_length=20, choices=MONTHS, verbose_name="Oy", null=True, blank=True,)
    year = models.IntegerField(default=timezone.now().year, verbose_name="Yil", null=True, blank=True,)
    amount = models.DecimalField(max_digits=11, decimal_places=2, verbose_name="Summa")
    comment = models.TextField(null=True, blank=True, verbose_name="Izoh")
    
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount} so'm"


