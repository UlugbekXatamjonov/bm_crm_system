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
        fields = ['first_name', 'last_name', 'slug', 'photo' ]







""" -------------- Teacher section API -------------- """
class MW_Teachers_Serializer(serializers.ModelSerializer):
    """ Main website ning Teachers bo'limmi uchun serializer """

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'photo', 'subject', 'dagree', 'experience']




