from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle


from .models import Teacher, Worker
from .serializers import Teacher_Create_Serializer, Teacher_List_Serializer, Teacher_Detail_Serializer




""" -----------------  O'qtuvchilar uchun CRUD funksiyalari  ------------------- """
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teachers_list(request):
    """ O'qtuvchilar ro'yhatini qaytaradigan funksiya """
    
    try:
        teachers = Teacher.objects.all()
        serializer = Teacher_List_Serializer(teachers, many=True, context={'request':request})
        
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




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def teacher_create(request):
    """ Yangi o'qituvchi va User qo'shish uchun funksiya. """
    
    serializer = Teacher_Create_Serializer(data=request.data)
    if serializer.is_valid():
        serializer.save()        
        return Response(
            {'data':f"Yangi o'qtuvchi {serializer.data['user']['first_name']} {serializer.data['user']['last_name']} muvaffaqiyatli qo'shildi"},
            status=status.HTTP_201_CREATED)
        
    return Response({'error':f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)









""" -----------------  Xodimlar uchun CRUD funksiyalari  ------------------- """





