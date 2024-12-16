from django.contrib import admin

from .models import Announcement, Parents_opinion, Contact_us

# Register your models here.


@admin.register(Announcement)
class Announcement_Admin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_on']
    list_filter = ['status', 'created_on']


@admin.register(Parents_opinion)
class Parents_opinion_Admin(admin.ModelAdmin):
    list_display = ['name', 'status']
    list_filter = ['status', 'created_on']


@admin.register(Contact_us)
class Contect_us_Admin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'status', 'created_on']
    list_filter = ['status', 'created_on']








