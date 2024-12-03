from django.contrib import admin

from .models import Weeky_exam_photos, Quarter_winners

# Register your models here.

@admin.register(Weeky_exam_photos)
class Weeky_exam_photos_Admin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_on']


@admin.register(Quarter_winners)
class Quarter_winners_Admin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_on']






