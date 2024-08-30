from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'passport')
    list_filter = ('status', 'gender')
    ordering = ('created_at',)
