from django.urls import path
from .views import create_teacher, list_teachers

urlpatterns = [
    # O'qituvchi URL'lari
    path('teachers/list/', list_teachers, name='teacher-list'),
    path('teachers/create/', create_teacher, name='teacher-create'),
    
    ]
