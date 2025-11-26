from django.urls import path
from .views import teacher_create, teachers_list, teacher_detail

urlpatterns = [
    # O'qituvchi URL'lari
    path('teachers/create/', teacher_create, name='teacher-create'),
    path('teachers/list/', teachers_list, name='teacher-list'),
    path('teachers/<slug:slug>/', teacher_detail, name='teacher-detail'),
    
]





