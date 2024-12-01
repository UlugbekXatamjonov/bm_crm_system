from rest_framework import serializers

from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia


""" -------------- Home page API -------------- """
class MW_HPA_Teachers_Serializer(serializers.ModelSerializer):
    """ MW_HPA --> Main Website Home Page Api
        Main websit ning Homepage dagi teachers bo'limi uchun serializer 
    """

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'photo' ]




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


