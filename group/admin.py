from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'teacher')
    search_fields = ('class_name', )
