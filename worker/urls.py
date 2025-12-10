from django.urls import path
# from .views import teachers_list #,  teacher_create, teacher_detail

# urlpatterns = [
#     # O'qituvchi URL'lari
#     # path('teachers/create/', teacher_create, name='teacher-create'),
#     # path('teachers/list/', teachers_list, name='teacher-list'),
#     # path('teachers/<slug:slug>/', teacher_detail, name='teacher-detail'),
    
# ]



from django.urls import path
from .views import (
    TeacherListAPIView,
    TeacherDetailAPIView,
    TeacherCreateAPIView,
    TeacherUpdateAPIView,
    TeacherDeleteAPIView,
)

urlpatterns = [
    path("teacher/", TeacherListAPIView.as_view(), name="teacher_list" ),


    # --------------------------------------------------------------
    # 2) TEACHER DETAIL — GET (slug orqali 1 dona teacher)
    # --------------------------------------------------------------
    path(
        "teacher/<slug:slug>/",
        TeacherDetailAPIView.as_view(),
        name="teacher_detail"
    ),
    # Slugdan foydalanish:
    # — SEO friendly, professional URL
    # — Userga eslab qolish oson
    # /api/teachers/john-doe/

    # --------------------------------------------------------------
    # 3) TEACHER CREATE — POST
    # --------------------------------------------------------------
    path(
        "teacher/create/",
        TeacherCreateAPIView.as_view(),
        name="teacher_create"
    ),
    # Alohida create endpoint:
    # /api/teachers/create/
    # — professional REST struktura emas (restda POST /teachers/ deyish kifoya),
    #   ammo sizning loyihangizda ko‘p ishlatilgani uchun qoldirdim.

    # --------------------------------------------------------------
    # 4) TEACHER UPDATE — PUT / PATCH
    # --------------------------------------------------------------
    path(
        "teacher/<slug:slug>/update/",
        TeacherUpdateAPIView.as_view(),
        name="teacher_update"
    ),
    # /api/teachers/john-doe/update/
    # PUT yoki PATCH ikkalasi ham qo‘llab-quvvatlanadi.

    # --------------------------------------------------------------
    # 5) TEACHER DELETE — DELETE
    # --------------------------------------------------------------
    path(
        "teacher/<slug:slug>/delete/",
        TeacherDeleteAPIView.as_view(),
        name="teacher_delete"
    ),
    # /api/teachers/john-doe/delete/
]


