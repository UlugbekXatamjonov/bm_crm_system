from rest_framework import status
# from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle

from django_filters import rest_framework as filters # type: ignore

from .models import Teacher, Worker
from .serializers import Teacher_Create_Serializer, Teacher_List_Serializer, Teacher_Detail_Serializer




""" -----------------  O'qtuvchilar uchun CRUD funksiyalari  ------------------- """
class Teacher_list_filters(filters.FilterSet):
    """ O'qituvchilar bo'limi uchun filterlar. """
    
    science = filters.CharFilter(field_name='science__name', lookup_expr='icontains', label="Fan nomi")
    # ❗ Agar modelda CharField maydoni da choises ishlatilgan bo'lsa, filterlshda  lookup_expr='exact' bo'lishi shart
    gender = filters.CharFilter(field_name='user__gender', lookup_expr='exact', label="Jinsi") 
    is_class_leader = filters.BooleanFilter(field_name='is_class_leader', label="Sinf rahbarligi") 
    is_mainpage = filters.BooleanFilter(field_name='is_mainpage', label="Asosiy saytda chiqishi") 

    class Meta:
        model = Teacher
        fields = ["science", "gender", "is_class_leader", "is_mainpage"]



@permission_classes([IsAuthenticated])
@api_view(['GET'])
def teachers_list(request):
    """ O'qituvchilar ro'yhatini qaytaradigan funksiya """
    try:
        filterset = Teacher_list_filters(request.GET, queryset=Teacher.objects.all())
        if not filterset.is_valid():
            return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = Teacher_List_Serializer(filterset.qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except:
        return Response({'error':"Ma'lumotlarni qayta ishlashhda xatolik yuzaga keldi !"}, status=status.HTTP_204_NO_CONTENT)    
    


@throttle_classes([AnonRateThrottle])
@api_view(["GET"])    
def teacher_detail(request, slug):
    """ Birdona o'qtuvchining ma'lumotlarini chiqarish uchun API """

    teacher = Teacher.objects.filter(slug=slug)
    serializer = Teacher_Detail_Serializer(teacher, many=True, context={'request':request})
    
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def teacher_create(request):
    """ Yangi o'qituvchi va User qo'shish uchun funksiya. """
    
    print("-------------------------------------------")
    
    print(request.data)
    serializer = Teacher_Create_Serializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()        
        return Response(
            {'data':f"Yangi o'qtuvchi {serializer.data['user']['first_name']} {serializer.data['user']['last_name']} muvaffaqiyatli qo'shildi"},
            status=status.HTTP_201_CREATED)
        
    return Response({'error':f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)









""" -----------------  Xodimlar uchun CRUD funksiyalari  ------------------- """





