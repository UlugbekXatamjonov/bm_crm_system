from rest_framework import serializers

from users.models import CustomUser
from users.serializers import CustomUser_Create_Serializer, CustomUser_List_Serializer, CustomUser_datas_for_Teachers_list_Serializer

from .models import Teacher, Worker, Teacher_Certificate, Teacher_SocialMedia



""" --------------------- Teacher Section ---------------------  """
class Teacher_Certificate_Serializer(serializers.ModelSerializer):
    """ O'qtuvchining sertifikatlari uchun serializer """

    class Meta:
        model = Teacher_Certificate
        fields = ['name', 'slug']


class Teacher_SM_Serializer(serializers.ModelSerializer):
    """ O'qtuvchining sertifikatlari uchun serializer """

    class Meta:
        model = Teacher_SocialMedia
        fields = ['name', 'slug']


class Teacher_Create_Serializer(serializers.ModelSerializer):
    """
    O'qtuvchi qo'shish uchun serializer.
    CustomUserSerializer() orqali bir vaqtning o'zida yangi User ham qo'shilib, u asosida Teacher obyetki ham qo'shiladi
    """
    user = CustomUser_Create_Serializer()  # Yangi user qo'shish uchun CustomUser serializerini ishlatamiz

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

        
class Teacher_List_Serializer(serializers.ModelSerializer):
    """ O'qtuvchilar ro'yhari uchun Serializer """
    
    user = CustomUser_datas_for_Teachers_list_Serializer()  # User malumotlarini olish uchun ushbu serializerni ishlatamiz 

    science_name = serializers.CharField(source='science.name')
    science_slug = serializers.CharField(source='science.slug')
    
    group_name_field = serializers.SerializerMethodField()
    group_slug_field = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['user', 'slug', 'photo', 'science_name', 'science_slug', 'is_class_leader', 
                    'group_name_field', 'group_slug_field']


    def get_group_name_field(self, obj):
        """ O'qituvchining guruhining nomini qaytaradi """
        
        group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
        if group_instance: # agar o'qtuvchining sinfi bo'lsa
            return group_instance.class_name # sinfning nomini qaytaramiz
        else:
            return None #Aks holda bo'sh qiymat qaytaramiz
    
    def get_group_slug_field(self, obj):
        """ O'qituvchining guruhining slugini qaytaradi """
        
        group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
        if group_instance: # agar o'qtuvchining sinfi bo'lsa
            return group_instance.slug # sinfning nomini qaytaramiz
        else:
            return None #Aks holda bo'sh qiymat qaytaramiz


class Teacher_Detail_Serializer(serializers.ModelSerializer):
    """ Birdona o'qtuvchining ma'lumotlarini chiqarish uchun serializer """

    user = CustomUser_List_Serializer()
    teacher_certificates = Teacher_Certificate_Serializer(many=True, read_only=True)
    # teacher_sms = Teacher_SM_Serializer(many=True, read_only=True)

    science_name = serializers.CharField(source='science.name')
    science_slug = serializers.CharField(source='science.slug')
    
    group_name = serializers.SerializerMethodField()
    group_slug = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = ["user", "slug", "photo", "passport_photo", "dagree", "experience", "start_time", 
                    "science_name", "science_slug", "group_name", "group_slug",   
                    "is_class_leader", "is_mainpage",
                    "teacher_certificates"
                ]

    
    def get_group_name(self, obj):
        """ O'qituvchining guruhining nomini qaytaradi """
        
        group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
        if group_instance: # agar o'qtuvchining sinfi bo'lsa
            return group_instance.class_name # sinfning nomini qaytaramiz
        else:
            return None #Aks holda bo'sh qiymat qaytaramiz
    
    def get_group_slug(self, obj):
        """ O'qituvchining guruhining slugini qaytaradi """
        
        group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
        if group_instance: # agar o'qtuvchining sinfi bo'lsa
            return group_instance.slug # sinfning nomini qaytaramiz
        else:
            return None #Aks holda bo'sh qiymat qaytaramiz




""" --------------------- Worker Section ---------------------  """
class WorkerSerializer(serializers.ModelSerializer):
    """
    Xodim (Worker) modeliga oid serializer.
    - Bu serializer Worker modelidagi barcha maydonlarni o'z ichiga oladi.
    """

    class Meta:
        model = Worker
        fields = ['id', 'user', 'photo', 'is_superadmin', 'salary']





