# Generated by Django 5.1 on 2024-08-28 16:45

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('student', '0001_initial'),
        ('worker', '0003_alter_teacher_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.today, null=True, verbose_name='Sana')),
                ('came', models.BooleanField(default=False, verbose_name='Keldi/Kelmadi')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Izoh')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.student', verbose_name="O'quvchi")),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worker.teacher', verbose_name="O'qtuvchi")),
                ('worker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='worker.worker', verbose_name='Hodim')),
            ],
        ),
    ]
