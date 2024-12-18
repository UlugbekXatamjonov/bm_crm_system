from django.contrib import admin

from .models import Parents_opinion, Contact_us,  Graduation_year, Graduate

# Register your models here.


# @admin.register(Announcement)
# class Announcement_Admin(admin.ModelAdmin):
#     list_display = ['name', 'status', 'created_on']
#     list_filter = ['status', 'created_on']


@admin.register(Parents_opinion)
class Parents_opinion_Admin(admin.ModelAdmin):
    list_display = ['name', 'status']
    list_filter = ['status', 'created_on']


@admin.register(Contact_us)
class Contect_us_Admin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'status', 'created_on']
    list_filter = ['status', 'created_on']

@admin.register(Graduation_year)
class Graduation_year_Admin(admin.ModelAdmin):
    list_display = ['year','number_of_graduates','number_of_enrollees','status']
    list_filter = ['status', 'created_on']


@admin.register(Graduate)
class Graduate_Admin(admin.ModelAdmin):
    list_display = ['name', 'graduation_year', 'university', 'status']
    list_filter = ['status', 'graduation_year', 'created_on']    




