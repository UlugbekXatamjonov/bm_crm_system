from django.urls import path

from .views import mw_mainpage_teachers_list, mw_mainpage_statistic_datas, \
        mw_teachers_section_list, mw_mainpage_students_certificate, mw_student_certificate_section_list,\
        mw_mainpage_sciences_list, mw_mainpage_weekly_exam_photos_list, mw_mainpage_quarter_winners_list,\
        contact_create, mw_mainpage_parents_opinion, graduation_years_list


"""--------- Mainpage paths --------- """
urlpatterns = [
    # Main page APIs path
    path('home-page/teachers/', mw_mainpage_teachers_list),
    path('home-page/stats/', mw_mainpage_statistic_datas),
    path('home-page/results/', mw_mainpage_students_certificate),
    path('home-page/sciences/', mw_mainpage_sciences_list),
    path('home-page/exams/', mw_mainpage_weekly_exam_photos_list),
    path('home-page/quarter_winners/', mw_mainpage_quarter_winners_list),
    path('home-page/opinions/', mw_mainpage_parents_opinion),
    
    # Sections paths
    path('teachers/', mw_teachers_section_list), 
    path('results/', mw_student_certificate_section_list),
    path('graduates/', graduation_years_list),
    path('contact/', contact_create),


    # path('annons/<slug:slug>/', announcement_detail),
    # path('annons/', announcement_list),
]








