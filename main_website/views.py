from django.shortcuts import render
from datetime import datetime
from django.db.models import Sum

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


from django_filters import rest_framework as filters # type: ignore


from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia, Worker
from student.models import Student, Student_Certificate
from science.models import Science
from exam.models import Weeky_exam_photos, Quarter_winners

from .models import Contact_us, Parents_opinion, Graduate, Graduation_year


from .serializers import MW_HPA_Teachers_Serializer, MW_Teachers_Serializer, MW_HPA_Statistic_Data_Serializer,\
    MW_HPA_Students_Certificate_Serializer, MW_Student_Certificate_Serializer, MW_HPA_Science_Serializer,\
    MW_HPA_Weeky_Exam_Photos_Serializer, MW_HPA_Quarter_winners_Serializer, Contact_us_Serializer,\
    MW_HPA_Parents_opinion_Certificate_Serializer, Graduation_year_Serializer


""" --------------- Loggs  ------------------ """
import logging
main_website_logger = logging.getLogger('main_website_logger')

""" --------------- Loggs  ------------------ """



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
    graduates - Bitiruvchilar soni
    enrollees - O'qishga kirganlar soni
    enrollment_rate - O'qishga kirish foizi
    """ 
    
    try:
        yearly_experiense = datetime.now().year - 2023 # yil o'tgani sari o'zgaruvchi qiymati aftomatik oshib boradi
        students_count = Student.objects.filter(user__status=True).count()
        banchs_count = 2 # ❗❗❗ Bu o'zgaruvchi "qo'lda" o'zgartiriladi ❗❗❗ 
        teachers_count = Teacher.objects.filter(user__status=True).count()
        
        # Bitiruvchilar haqidagi ma'lumotlar yig'iladi
        graduation_data = Graduation_year.objects.filter(status=True).aggregate(
            total_enrollees=Sum('number_of_enrollees'),
            total_graduates=Sum('number_of_graduates')
        )
        
        enrollees = graduation_data.get('total_enrollees') or 0
        graduates = graduation_data.get('total_graduates') or 0

        # O'qishga kirish foizi
        enrollment_rate = round((enrollees * 100 / graduates), 2) if graduates > 0 else 0

        data = [{
            "yearly_experiense" : yearly_experiense,
            "students_count" : students_count,
            "banchs_count" : banchs_count,
            "teachers_count" : teachers_count,
            "graduates":graduates,
            "enrollees":enrollees,
            "enrollment_rate" : enrollment_rate,
        }]
    
        serializer = MW_HPA_Statistic_Data_Serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)

        """ serializer.data[0] --> yuborilayotgan data ro'yhat bo'lib qoldi uni tsiklda bo'masligi uchun,
            [0] elementni o'zini yuboriladi."""
        return Response(serializer.data[0], status=status.HTTP_200_OK)
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga statistika chiqarishda xatolik bo'ldi: {e}")
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
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga fanlar ro'yhatini chiqarishda xatolik bo'ldi: {e}")
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
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga haftalik imtihonlar rasmlarini chiqarishda xatolik bo'ldi: {e}")
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
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga choraklik g'oliblari rasmini chiqarishda xatolik bo'ldi: {e}")
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
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga o'qtuvchilar ro'yhatini chiqarishda xatolik bo'ldi: {e}")
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
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga o'quvchilar natijasini chiqarishda xatolik bo'ldi: {e}")
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
       

@api_view(["GET"])
@throttle_classes({AnonRateThrottle})
def mw_mainpage_parents_opinion(request):
    """ Ota-onalar fikri uchun API 
    So'rov turi: GET
    Maydonlar:
    name - ota-ona ismi
    opinion - fikr matni
    photo - rasm
    """
    
    try:
        opinons = Parents_opinion.objects.filter(status=True)
        serializer = MW_HPA_Parents_opinion_Certificate_Serializer(opinons, many=True, context={'request':request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except Exception as e:
        # main_website_logger.error(f"Asosiy sahifaga ota-onalar fikrini chiqarishda xatolik bo'ldi: {e}")
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
    



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

    except Exception as e:
        # main_website_logger.error(f"O'qtuvchilar bo'limida, o'qtuvchilar ro'yhatini chiqarishda xatolik bo'ldi: {e}")
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
    


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
        # main_website_logger.error(f"Result bo'limida, natijalar chiqarishda xatolik bo'ldi: {e}")
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
    


""" -------------- Announcement section API -------------- """
# @throttle_classes([AnonRateThrottle])
# @api_view(['GET'])
# def announcement_list(request):
#     """ E'lonlar bo'limi uchun API ro'yhati 
#         name - E'lon nomi
#         slug - bitta e'longa kirish uchun kalit
#         about - e'lon matni
#         photo - e'lon rasm
#         created_on - e'lon yozilgan vaqti
#     """
    
#     try:
#         announcements = Announcement.objects.filter(status=True)
#         serializer = Announcement_Serializer(announcements, many=True, context={'request': request})
    
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except:
#         return Response({'error':""})
    
    
# @throttle_classes([AnonRateThrottle])
# @api_view(['GET'])    
# def announcement_detail(request, slug):
#     """  E'lonlar bo'limida yakka e'longa kirish uchun API 
#         name - E'lon nomi
#         slug - bitta e'longa kirish uchun kalit
#         about - e'lon matni
#         photo - e'lon rasm
#         created_on - e'lon yozilgan vaqti
#     """
    
#     announcement = Announcement.objects.filter(status=True, slug=slug)
#     serializer = Announcement_Serializer(announcement, many=True, context={'request':request})
    
#     return Response(serializer.data, status=status.HTTP_200_OK)
    

    
""" --------------  Graduates section API -------------- """
@api_view(["GET"])
@throttle_classes({AnonRateThrottle})
def graduation_years_list(request):
    """ Bitiruvchilar haqida ma'lumotlar
    So'rov turi: GET
    Maydonlar:
        year - Bitirgan yili
        number_of_graduates - Bitiruvchilar soni
        number_of_enrollees - O'qishga kirganlar soni
        graduates - Bitiruvchi haqidagi ma'lumotlar(array)
        name - ismi
        university - universitet nomi
        photo - rasmi
    """

    try:
        graduation_years = Graduation_year.objects.filter(status=True)
        serializer = Graduation_year_Serializer(graduation_years, many=True, context={'request':request})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
  
    except Exception as e:
        # main_website_logger.error(f"Bitiruvchilar bo'limiga ma'lumot chiqarishda xatolik bo'ldi: {e}")
        return Response({'error':"Ma'lumotlarni qayta ishlashda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)
    


""" -------------- Contact us section API -------------- """
@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def contact_create(request):
    """ Yangi xabar qo'shish uchun funksiya. 
    So'rob turi: POST
    Maydonlar:
    name - ism familiya 
    phone - telefon raqam
    """
    
    serializer = Contact_us_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()        
        return Response(
            {'data':f"Xabaringiz muvaffaqiyatli yuborildi !"}, status=status.HTTP_201_CREATED)
    
    
    # main_website_logger.error(f"Contact us dan xabar kelishida xatolik bo'ldi: {e}")   
    return Response({'error':"Ma'lumotlarni tuborishda xatolik yuzaga keldi"}, status=status.HTTP_400_BAD_REQUEST)


    
    
    
    
    
    
    
    