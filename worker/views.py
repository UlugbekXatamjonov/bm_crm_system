from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle


from .models import Teacher, Worker
from .serializers import TeacherSerializer




""" -----------------  O'qtuvchilar uchun CRUD funksiyalari  ------------------- """

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_teacher_with_user(request):
    """ Yangi o'qituvchi va User qo'shish uchun funksiya. """
    
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()        
        return Response(
            {'data':f"Yangi o'qtuvchi {serializer.data['user']['first_name']} {serializer.data['user']['last_name']} muvaffaqiyatli qo'shildi"},
            status=status.HTTP_201_CREATED)
        
    return Response({'error':f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)









""" -----------------  Xodimlar uchun CRUD funksiyalari  ------------------- """





