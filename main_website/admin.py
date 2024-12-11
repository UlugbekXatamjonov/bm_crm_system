from django.contrib import admin

from .models import Announcement

# Register your models here.


@admin.register(Announcement)
class Announcement_Admin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_on']
    list_filter = ['status', 'created_on']














