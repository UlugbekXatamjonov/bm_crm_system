from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date',  'came', 'student', 'teacher', 'worker')
    
    search_fields = (
        'student__user__first_name', 'student__user__last_name', 'student__user__passport', \
        'teacher__user__first_name', 'teacher__user__last_name', 'teacher__user__passport', \
        'worker__user__first_name', 'worker__user__last_name', 'worker__user__passport', \
        'date', "comment"
        )
    
    list_filter = ('came', 'date', 'student__group')
