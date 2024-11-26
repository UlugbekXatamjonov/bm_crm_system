from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend


from .serializers import MW_HPA_Teachers_Serializer
from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia

# Create your views here.


class MW_HPA_Teachers_Viewset(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = MW_HPA_Teachers_Serializer
    lookup_field = 'slug'
        
    # throttle_classes = [AnonRateThrottle]   
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['group', 'plase']
    # search_fields = ['name',]









