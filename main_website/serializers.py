from rest_framework import serializers

from worker.models import Teacher, Teacher_Certificate, Teacher_SocialMedia


""" 
MW - Main Website 
HPA - Home page API 

"""


""" -------------- Home page API -------------- """
class MW_HPA_Teachers_Serializer(serializers.ModelSerializer):
    """ O'qituvchi modeliga oid serializer.
        - Bu serializer Teacher modelidagi barcha maydonlarni o'z ichiga oladi.
    """

    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Teacher
        fields = ['slug', 'first_name', 'last_name', 'photo' ]

















