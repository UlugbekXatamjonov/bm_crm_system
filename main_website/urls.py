from django.urls import path

from .views import MW_HPA_Teachers_Viewset



"""--------- Mainpage paths --------- """

urlpatterns = [
    path('', MW_HPA_Teachers_Viewset.as_view({'get':"list"}), name='mainpage-teachers'),
]






