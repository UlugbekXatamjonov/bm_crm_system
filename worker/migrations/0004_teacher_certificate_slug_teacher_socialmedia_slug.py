# Generated by Django 5.1 on 2024-12-12 05:59

import autoslug.fields
import worker.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('worker', '0003_remove_teacher_salary_remove_worker_salary'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher_certificate',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from=worker.models.slug_funckion_for_teacher_certificate, unique=True),
        ),
        migrations.AddField(
            model_name='teacher_socialmedia',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, null=True, populate_from=worker.models.slug_funckion_for_teacher_social_media, unique=True),
        ),
    ]
