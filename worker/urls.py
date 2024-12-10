from django.urls import path
from .views import create_teacher_with_user

urlpatterns = [
    # O'qituvchi URL'lari
    path('teachers/create/', create_teacher_with_user, name='teacher-create'),
    
    ]
