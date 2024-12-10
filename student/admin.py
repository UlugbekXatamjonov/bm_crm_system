from django.contrib import admin
from .models import Student, Father_and_Mother, Student_Certificate 


# @admin.register(Student_Certificate)
class Student_Certificate_Admin(admin.TabularInline):
    model = Student_Certificate
    list_display = ('name', 'photo', 'about', 'status', '')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'group', "user__passport", "is_discount", "discount_amount")
    search_fields = ('user__first_name', 'user__last_name', "user__passport")
    list_filter = ('group', "is_discount", "discount_amount")
    inlines = [Student_Certificate_Admin, ]


@admin.register(Father_and_Mother)
class FatherAndMotherAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__phone1', 'user__phone2', 'user__passport')
    
    search_fields = (
        'user__first_name', 'user__last_name', "user__passport",\
        'mother_full_name', 
    )
