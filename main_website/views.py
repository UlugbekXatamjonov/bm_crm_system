from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from datetime import datetime
from django_filters import rest_framework as filters


from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia, Worker
from student.models import Student, Student_Certificate
from science.models import Science
from exam.models import Weeky_exam_photos, Quarter_winners
from .models import Announcement


from .serializers import MW_HPA_Teachers_Serializer, MW_Teachers_Serializer, MW_HPA_Statistic_Data_Serializer,\
    MW_HPA_Students_Certificate_Serializer, MW_Student_Certificate_Serializer, MW_HPA_Science_Serializer,\
    MW_HPA_Weeky_Exam_Photos_Serializer, MW_HPA_Quarter_winners_Serializer, Announcement_Serializer



# Create your views here.
""" -------------- Home page API -------------- """
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def mw_mainpage_statistic_datas(request):
    """
    Asosiy websaytning Homepage qismidagi statistika bo'limi uchun API 
    So'rov turi: GET
    
    Maydonlar:  
    yearly_experiense - tajriba yili
    students_count - o'quvchilar soni
    banchs_count - filiallar soni
    teachers_count - o'qtuvchilar soni
    """
    
    try:
        yearly_experiense = datetime.now().year - 2023 # yil o'tgani sari o'zgaruvchi qiymati aftomatik oshib boradi
        students_count = Student.objects.filter(user__status=True).count()
        banchs_count = 2 # ❗❗❗ Bu o'zgaruvchi "qo'lda" o'zgartiriladi ❗❗❗ 
        teachers_count = Teacher.objects.filter(user__status=True).count()
        
        data = [{
            "yearly_experiense" : yearly_experiense,
            "students_count" : students_count,
            "banchs_count" : banchs_count,
            "teachers_count" : teachers_count,
        }]
    except:
        return Response({'error': "Ma'lumotlarni to'plashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)    
    
    try:
        serializer = MW_HPA_Statistic_Data_Serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        """ serializer.data[0] --> yuborilayotgan data ro'yhat bo'lib qoldi uni tsiklda bo'masligi uchun,
            [0] elementni o'zini yuboriladi."""
        return Response(serializer.data[0], status=status.HTTP_200_OK)
    except:
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
    
 
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def mw_mainpage_sciences_list(request):
    """
    Asosiy websaytning Homepage qismidagi Iqtisoslik fanlari bo'limi uchun API 
    So'rov turi: GET
    
    Maydonlar:  
    name - fan nomi
    photo - fan rasmi
    about - fan  haqida
    """
    
    try:    
        science = Science.objects.filter(status=True, is_mainpage=True)
        serializer = MW_HPA_Science_Serializer(science, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def mw_mainpage_weekly_exam_photos_list(request):
    """
        Asosiy websaytning Homepage qismidagi Haftalik imtihonlar bo'limi uchun API 
        So'rov turi: GET
        
        Maydonlar:  
        photo - rasm
    """
    
    try:
        photos = Weeky_exam_photos.objects.filter(status=True)
        serializer = MW_HPA_Weeky_Exam_Photos_Serializer(photos, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
 
        
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def mw_mainpage_quarter_winners_list(request):
    """
        Asosiy websaytning Homepage qismidagi Chorak g'oliblari bo'limi uchun API 
        So'rov turi: GET
        
        Maydonlar:  
        photo - rasm
    """
    try:
        photos = Quarter_winners.objects.filter(status=True)
        serializer = MW_HPA_Quarter_winners_Serializer(photos, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
         
        
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
    try:
        teachers = Teacher.objects.filter(user__status=True, is_mainpage=True) # Filtrlangan querysetni olish
        serializer = MW_HPA_Teachers_Serializer(teachers, many=True, context={'request': request}) # Serializer orqali ma'lumotlarni formatlash
        
        return Response(serializer.data, status=status.HTTP_200_OK)  # Javobni qaytarish
    except:
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)

   
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def mw_mainpage_students_certificate(request):
    """
    Asosiy websaytning Homepage qismidagi O'quvchilarning natijalari bo'limi uchun API 
    So'rov turi: GET
    
    Maydonlar:  
    first_name - o'quvchining ismi  
    last_name - o'quvchining familiyasi
    student_photo - o'quvchining rasmi
    science_name - fan nomi
    name -  sertifikat nomi
    photo -  sertifikat rasmi
    about - sertifikat haqida
    """
    try:
        certificate = Student_Certificate.objects.filter(status=True, is_mainpage=True)
        serializer = MW_HPA_Students_Certificate_Serializer(certificate, many=True, context={'request': request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    except: 
        return Response({'error': "Ma'lumotlarni to'plashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)    
        



""" -------------- Teacher section API -------------- """
class TeacherFilter(filters.FilterSet):
    """ Teacher bo'limida o'qtuvchilarni fani bo'yicha filterlash uchun FilterSet """
    
    science_name = filters.CharFilter(field_name='science__name', lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['science_name']


@throttle_classes([AnonRateThrottle])
@api_view(['GET'])
def mw_teachers_section_list(request):  
    """
    Asosiy websaytning Teachers bo'limi uchun o'qtuvchilarning ro'yhatini uchun API
    So'rov turi: GET
    Filterlash uchun  --> teachers/?science_name=Fan nomi
  
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
    
    try:
        # Foydalanuvchidan kelgan so‘rovni filtrlash
        filterset = TeacherFilter(request.GET, queryset=Teacher.objects.filter(user__status=True))
        if not filterset.is_valid(): # validatsiyadan o'tkazish
            return Response({'error': 'Filtr parametrlari noto\'g\'ri'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MW_Teachers_Serializer(filterset.qs, many=True, context={'request': request}) # filterset.qs --> qs o'zgarmas key
        return Response(serializer.data, status=status.HTTP_200_OK)

    except:
        return Response({'error': f"Ma'lumotlarni qayta ishlashda xatolik yuz berdi: "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




""" -------------- Result section API -------------- """
class StudentCertificateFilter(filters.FilterSet):
    science_name = filters.CharFilter(field_name='science__name', lookup_expr='icontains', label="Fan nomi")

    class Meta:
        model = Student_Certificate
        fields = ['science_name']


@throttle_classes([AnonRateThrottle])
@api_view(['GET'])
def mw_student_certificate_section_list(request):
    """
    Asosiy websaytning Natijalar bo'limi uchun API 
    So'rov turi: GET

    Maydonlar:  
    first_name - o'quvchining ismi  
    last_name - o'quvchining familiyasi
    student_photo - o'quvchining rasmi
    science_name - fan nomi
    name -  sertifikat nomi
    photo -  sertifikat rasmi
    about - sertifikat haqida
    """
    
    try:
        filterset = StudentCertificateFilter(request.GET, queryset=Student_Certificate.objects.filter(status=True))
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = MW_Student_Certificate_Serializer(filterset.qs, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f"Ma'lumotlarni qayta ishlashda xatolik yuz berdi: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



""" -------------- Announcement section API -------------- """
@throttle_classes([AnonRateThrottle])
@api_view(['GET'])
def announcement_list(request):
    """ E'lonlar bo'limi uchun API """
    
    announcements = Announcement.objects.filter(status=True)
    serializer = Announcement_Serializer(announcements, many=True, context={'request': request})
    
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    