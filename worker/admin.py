from django.contrib import admin
from .models import Teacher, Worker, Teacher_Certificate, Teacher_SocialMedia

""" ------- O'qtuvchi uchun adminlar  ------- """
class Teacher_Certificate_Admin(admin.TabularInline):
    model = Teacher_Certificate
    list_display = ('name',)
    
    
class Teacher_SocialMedia_Admin(admin.TabularInline):
    model = Teacher_SocialMedia
    fields = ('name', 'url')


@admin.register(Teacher)
class Teacher_Admin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'science', 'is_class_leader')
    search_fields = ('user__first_name', 'user__last_name', 'science')
    list_filter = ('is_class_leader', "science", 'user__gender')
    inlines = [Teacher_Certificate_Admin, Teacher_SocialMedia_Admin]



""" ------- Xodimlar uchun adminlar  ------- """
@admin.register(Worker)
class Worker_Admin(admin.ModelAdmin):
    list_display = ('user__first_name', 'user__last_name', 'is_superadmin')
    search_fields = ('user__first_name', 'user__last_name')
    list_filter = ('is_superadmin', 'user__gender')





