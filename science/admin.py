from django.contrib import admin

from .models import Science

# Register your models here.

@admin.register(Science)
class Science_Admin(admin.ModelAdmin):
    list_display = ['name', 'is_mainpage', 'status']
    
    
    
    
    