from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from .serializers import MW_HPA_Teachers_Serializer, MW_Teachers_Serializer
from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia


# Create your views here.
    
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])  # Faqat ushbu funksiya uchun AnonRateThrottle ni yoqish
def mw_mainpage_teachers_list(request):
    """ 
    Asosiy websaytning Homepage qismidagi teachers bo'limi uchun API 
    So'rov turi: GET
    
    Maydonlar:  
    first_name - ism 
    last_name - familiya
    photo - o'qtuvchining rasmi
    """
    
    teachers = Teacher.objects.filter(user__status=True, is_mainpage=True) # Filtrlangan querysetni olish
    serializer = MW_HPA_Teachers_Serializer(teachers, many=True) # Serializer orqali ma'lumotlarni formatlash
    
    return Response(serializer.data, status=status.HTTP_200_OK)  # Javobni qaytarish


@throttle_classes([AnonRateThrottle])
@api_view(['GET'])
def mw_teachers_section_list(request):
    """ Asosiy websaytning Teachers bo'limi uchun o'qtuvchilarning ro'yhatini uchun API
        So'rov turi: GET
        
        Maydonlar:
        first_name - ism 
        last_name - familiya
        photo - o'qtuvchining rasmi
        dagree - o'qtuvchining ma'lumoti
        experience - o'qtuvchining tajribasi
        science_name - fan nomi
        science_slug - fanning slugi(fan ustiga bosilganda fanlar bo'limidagi shu fanga o'tishi uchun)        
        --------------
        teacher_sm - o'qtuvchining ijtimoiy tarmoqlardagi sahifalari
            name - ijtmoiy tarmoq nomi
            url - ijtmoiy tarmoq manzili
        --------------
        teacher_certificate - o'qtuvchining sertifikatlari
            name - sertifikat nomi
            photo - sertifikat rasmi
    """

    teachers = Teacher.objects.filter(user__status = True)
    serializer = MW_Teachers_Serializer(teachers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)










