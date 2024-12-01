from django.urls import path

from .views import mw_mainpage_teachers_list, mw_teachers_section_list


"""--------- Mainpage paths --------- """
urlpatterns = [
    # path('home-page/teachers/', MW_HPA_Teachers_Viewset.as_view({'get':"list"})),
    
    # Main page APIs path
    path('home-page/teachers/', mw_mainpage_teachers_list),
    
    
    # Sections paths
    path('teachers/', mw_teachers_section_list), 
    
]






