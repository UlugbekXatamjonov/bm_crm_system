from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from django_filters.rest_framework import DjangoFilterBackend


from .serializers import MW_HPA_Teachers_Serializer, MW_Teachers_Serializer
from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia


# Create your views here.
    
@api_view(['GET'])
def mw_mainpage_teachers_list(request):
    """ Main websitning Homepage dagi teachers bo'limi uchun GET API """
    
    teachers = Teacher.objects.filter(user__status=True, is_mainpage=True) # Filtrlangan querysetni olish
    serializer = MW_HPA_Teachers_Serializer(teachers, many=True) # Serializer orqali ma'lumotlarni formatlash
    
    return Response(serializer.data, status=status.HTTP_200_OK)  # Javobni qaytarish


@api_view(['GET'])
def mw_teachers_section_list(request):
    """ Main websitning Teachers bo'limi uchun o'qtuvchilarning ro'yhatini qaytaradi"""

    teachers = Teacher.objects.filter(user__status = True)
    serializer = MW_Teachers_Serializer(teachers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

