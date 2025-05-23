# Generated by Django 5.1 on 2024-12-02 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses_type', models.CharField(choices=[('utility_bills', "Komunal to'lovlar"), ('monthly salaries', 'Maoshlar'), ('foods', 'Oziq ovqat'), ('construction', 'Tamirlash va qurilish'), ('educational_tools', 'Kanstovar'), ('construction', 'Qurilish'), ('furniture', 'Mebellar')], max_length=30, verbose_name='Xarajat turi')),
                ('title', models.CharField(max_length=250, verbose_name='Nomi')),
                ('month', models.CharField(blank=True, choices=[('january', 'Yanvar'), ('february', 'Fevral'), ('march', 'Mart'), ('april', 'Aprel'), ('may', 'May'), ('june', 'Iyun'), ('july', 'Iyul'), ('august', 'Avgust'), ('september', 'Sentyabr'), ('october', 'Oktyabr'), ('november', 'Noyabr'), ('december', 'Dekabr')], max_length=20, null=True, verbose_name='Oy')),
                ('year', models.IntegerField(blank=True, default=2024, null=True, verbose_name='Yil')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Summa')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Izoh')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('student_payment', "Oylik to'lov"), ('other_income', 'Boshqa daromad')], default='student_payment', max_length=20, verbose_name='Daromad turi')),
                ('month', models.CharField(choices=[('january', 'Yanvar'), ('february', 'Fevral'), ('march', 'Mart'), ('april', 'Aprel'), ('may', 'May'), ('june', 'Iyun'), ('july', 'Iyul'), ('august', 'Avgust'), ('september', 'Sentyabr'), ('october', 'Oktyabr'), ('november', 'Noyabr'), ('december', 'Dekabr')], max_length=20, verbose_name='Oy')),
                ('year', models.IntegerField(default=2024, verbose_name='Yil')),
                ('amount_due', models.DecimalField(blank=True, decimal_places=2, default=2500000, max_digits=10, null=True, verbose_name="To'lov qilinishi kerak bo'lgan summa")),
                ('paid_amount', models.DecimalField(decimal_places=2, default=2500000, max_digits=10, verbose_name="To'langan summa")),
                ('payment_status', models.CharField(blank=True, choices=[('unpaid', "To'lanmagan"), ('unfinished', 'Yakunlanmagan'), ('paid', "To'langan")], max_length=30, null=True, verbose_name="To'lov holati")),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student', verbose_name="O'quvchi")),
            ],
        ),
    ]
