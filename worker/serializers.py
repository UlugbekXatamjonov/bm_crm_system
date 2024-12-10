from rest_framework import serializers

from .models import Teacher, Worker
from users.models import CustomUser



""" --------------------- Teacher Section ---------------------  """

class CustomUserSerializer(serializers.ModelSerializer):
    """
    OnetoOneField bog'lanish bo'yicha ulangan modellarda O'qtuvchi, Xodim, O'quvchi, Ota-ona ni qo'shish vaqtida,
    CustomUser ni ham yaratib ketish uchun ushbu serializerdan foydalanildi.
    """
    
    class Meta:
        model = CustomUser
        fields = ['passport', 'password', 'email', 'first_name', 'last_name', 'date_of_bith', 'phone1', 'phone2', 
                    'gender', 'personal_status', 'address', 'status']



class TeacherSerializer(serializers.ModelSerializer):
    """
    O'qtuvchi qo'shish uchun serializer.
    CustomUserSerializer() orqali bir vaqtning o'zida yangi User ham qo'shilib, u asosida Teacher obyetki ham qo'shiladi
    """
    user = CustomUserSerializer()  # Yangi user qo'shish uchun CustomUser serializerini ishlatamiz

    class Meta:
        model = Teacher
        fields = ['user', 'slug', 'photo', 'passport_photo', 'salary', 'science', 'dagree', 'experience', 
                    'start_time', 'is_class_leader', 'is_mainpage']


    def create(self, validated_data):
        """
        Yangi o'qituvchi yaratishda, bir vaqtning o'zida CustomUser ni ham yaratish.
        """
        user_data = validated_data.pop('user')  # 'user' ma'lumotlarini ajratib olamiz
        user = CustomUser.objects.create(**user_data)  # CustomUser obyekti yaratamiz
        teacher = Teacher.objects.create(user=user, **validated_data)  # Teacher obyekti yaratamiz
        
        return teacher











""" --------------------- Worker Section ---------------------  """
class WorkerSerializer(serializers.ModelSerializer):
    """
    Xodim (Worker) modeliga oid serializer.
    - Bu serializer Worker modelidagi barcha maydonlarni o'z ichiga oladi.
    """

    class Meta:
        model = Worker
        fields = ['id', 'user', 'photo', 'is_superadmin', 'salary']

