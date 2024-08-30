from django.contrib import admin
from .models import Teacher, Worker

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'subject', 'is_class_leader')
    search_fields = ('user__first_name', 'user__last_name', 'subject')
    list_filter = ('is_class_leader', "subject", 'user__gender')

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'position', 'is_superadmin')
    search_fields = ('user__first_name', 'user__last_name', 'position')
    list_filter = ('is_superadmin', 'user__gender', 'position')





