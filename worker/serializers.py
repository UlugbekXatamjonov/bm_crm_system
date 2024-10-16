from rest_framework import serializers
from .models import Teacher, Worker

class TeacherSerializer(serializers.ModelSerializer):
    """
    O'qituvchi modeliga oid serializer.
    - Bu serializer Teacher modelidagi barcha maydonlarni o'z ichiga oladi.
    """

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'photo', 'salary', 'subject', 'is_class_leader', 'personal_status']

    # Foydalanuvchining to'liq ismini qaytarish uchun maxsus method qo'shamiz
    def get_full_name(self, obj):
        return obj.user.get_full_name()


class WorkerSerializer(serializers.ModelSerializer):
    """
    Xodim (Worker) modeliga oid serializer.
    - Bu serializer Worker modelidagi barcha maydonlarni o'z ichiga oladi.
    """

    class Meta:
        model = Worker
        fields = ['id', 'user', 'photo', 'position', 'is_superadmin', 'salary']
