from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField, IntegerField
from rest_framework.decorators import api_view
from rest_framework.response import Response

from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia
from student.models import Student, Student_Certificate
from science.models import Science
from exam.models import Weeky_exam_photos, Quarter_winners
from .models import Announcement


""" -------------- Home page API -------------- """
class MW_HPA_Statistic_Data_Serializer(Serializer):
    """ Main websayt ning Homepage qismidagi Statistik ma'lumotlar uchun serializer """
    yearly_experiense = IntegerField()
    students_count = IntegerField()
    banchs_count = IntegerField()
    teachers_count = IntegerField()


class MW_HPA_Science_Serializer(serializers.ModelSerializer):
    """ Main websayt ning Homepage qismidagi Iqtisoslik fanlari qismi uchun API """

    class Meta:
        model = Science
        fields = ['name', 'photo', 'about']


class MW_HPA_Weeky_Exam_Photos_Serializer(serializers.ModelSerializer):
    """ Main websayt ning Homepage qismidagi Haftalik imtihonlar qismi uchun API """
    
    class Meta:
        model = Weeky_exam_photos
        fields = ['photo',]


class MW_HPA_Quarter_winners_Serializer(serializers.ModelSerializer):
    """ Main websayt ning Homepage qismidagi Chorak g'oliblari qismi uchun API """

    class Meta:
        model =Quarter_winners
        fields = ['photo', ]


class MW_HPA_Teachers_Serializer(serializers.ModelSerializer):
    """ MW_HPA --> Main Website Home Page Api
        Main websayt ning Homepage dagi teachers bo'limi uchun serializer 
    """

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'photo' ]


class MW_HPA_Students_Certificate_Serializer(serializers.ModelSerializer):
    """ Main websayt ning Homepage qismidagi O'quvchilarning natijalari uchun serializer """
    
    first_name = serializers.CharField(source='student.user.first_name')
    last_name = serializers.CharField(source='student.user.last_name')
    student_photo = serializers.ImageField(source='student.photo')
    science_name = serializers.CharField(source='science.name')
    
    class Meta:
        model = Student_Certificate
        fields = ['first_name', 'last_name', 'student_photo', 'science_name', 'name', 'photo', 'about']


""" -------------- Teacher section API -------------- """
class MW_Teacher_Social_media_Serializer(serializers.ModelSerializer):
    """ Main website ning Teachers bo'limi APIlari, social media qismi uichun serializer """

    class Meta:
        model = Teacher_SocialMedia
        fields = ['name', 'url']


class MW_Teacher_Certificate_Serializer(serializers.ModelSerializer):
    """ Main website ning Teachers bo'limi APIlari, sertifikatlar qismi uichun serializer """

    class Meta:
        model = Teacher_Certificate
        fields = ['name', 'photo']


class MW_Teachers_Serializer(serializers.ModelSerializer):
    """ Main website ning Teachers bo'limmi uchun serializer """

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    
    science_name = serializers.CharField(source='science.name')
    science_slug = serializers.CharField(source='science.slug')

    teacher_sm = MW_Teacher_Social_media_Serializer(many=True, read_only=True)
    teacher_certificate = MW_Teacher_Certificate_Serializer(many=True, read_only=True)
        
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 
                'photo', 'dagree', 'experience', 
                'science_name', 'science_slug', 
                'teacher_sm', 'teacher_certificate']



""" -------------- Student Certificate section API -------------- """
class MW_Student_Certificate_Serializer(serializers.ModelSerializer):
    """ Main website ning Natijalar bo'limi APIlari """

    first_name = serializers.CharField(source='student.user.first_name')
    last_name = serializers.CharField(source='student.user.last_name')
    student_photo = serializers.CharField(source='student.photo')
    science_name = serializers.CharField(source='science.name')
    
    class Meta:
        model = Student_Certificate
        fields = ['first_name', 'last_name', 'student_photo', 'science_name', 'name', 'photo', 'about']



""" -------------- Announcement section API -------------- """
class Announcement_Serializer(serializers.ModelSerializer):
    """" E'lonlar bo'limi uchun serializer """
    created_on = serializers.DateTimeField(format="%Y-%m-%d | %H:%M:%S")  # Sana va vaqtga format belgilash

    class Meta:
        model = Announcement
        fields = ['name', 'slug', 'about', 'photo', 'created_on']













