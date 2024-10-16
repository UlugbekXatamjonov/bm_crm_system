from django.urls import path
from .views import TeacherListCreateAPIView, TeacherRetrieveUpdateDestroyAPIView, WorkerListCreateAPIView, WorkerRetrieveUpdateDestroyAPIView

urlpatterns = [
    # O'qituvchi URL'lari
    path('teachers/<int:pk>/', TeacherRetrieveUpdateDestroyAPIView.as_view(), name='teacher-detail'),
    path('teachers/', TeacherListCreateAPIView.as_view(), name='teacher-list-create'),

    # Xodim URL'lari
    path('workers/<int:pk>/', WorkerRetrieveUpdateDestroyAPIView.as_view(), name='worker-detail'),
    path('workers/', WorkerListCreateAPIView.as_view(), name='worker-list-create'),
]
