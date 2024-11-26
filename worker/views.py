from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated # type: ignore

from .models import Teacher, Worker
from .serializers import TeacherSerializer, WorkerSerializer

class TeacherListCreateAPIView(ListCreateAPIView):
    """
    O'qituvchilarni ro'yxatini olish va yangi o'qituvchi qo'shish.
    GET: Barcha o'qituvchilarni qaytaradi.
    POST: Yangi o'qituvchi yaratadi.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    O'qituvchini ko'rish, yangilash va o'chirish.
    GET: Bitta o'qituvchini qaytaradi.
    PUT/PATCH: O'qituvchini yangilaydi.
    DELETE: O'qituvchini o'chiradi.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Xodimlar CRUD funksiyalari

class WorkerListCreateAPIView(ListCreateAPIView):
    """
    Xodimlarni ro'yxatini olish va yangi xodim qo'shish.
    GET: Barcha xodimlarni qaytaradi.
    POST: Yangi xodim yaratadi.
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Xodimni ko'rish, yangilash va o'chirish.
    GET: Bitta xodimni qaytaradi.
    PUT/PATCH: Xodimni yangilaydi.
    DELETE: Xodimni o'chiradi.
    """
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







