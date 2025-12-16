""" Murakkab filterlar yasash uchun alohida fayl """


from django_filters import rest_framework as filters
from .models import Teacher


class TeacherFilter(filters.FilterSet):
    """ Teacher ning maydonlarini filterlash uchun  """
    
    gender = filters.CharFilter(field_name='user__gender', lookup_expr='exact') # ForeginKey maydonlari uchun
    personal_status = filters.CharFilter(field_name='user__personal_status', lookup_expr='exact') # ForeginKey maydonlari uchun
    status = filters.CharFilter(field_name='user__status', lookup_expr='exact')
    created_on = filters.CharFilter(field_name='user__created_on', lookup_expr='exact')


    class Meta:
        model = Teacher
        # Meta.fields da faqat asosiy modelning maydonlari (Teacher) bo'lishi kerak.
        # Related maydonlarni yuqorida alohida filter sifatida aniqlaymiz.
        fields = [
            'science',          # Teacher.science (FK) bo'lsa slug yoki id bilan filtrlash mumkin
            'experience',
            'is_class_leader',
            'is_mainpage',
        ]
