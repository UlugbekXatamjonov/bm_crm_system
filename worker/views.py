
from django_filters import rest_framework as filters # type: ignore
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Q
import logging

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from .models import Teacher, Worker
from .serializers import TeacherListSerializer, TeacherDetailSerializer
from .filters import TeacherFilter


# ---------------------------------------------------------
# Logger sozlamasi:
# - logger orqali muhim voqealar va xatoliklar filega yoki
#   monitoring tizimiga yozilishi mumkin.
# - productionda LOGGING konfiguratsiyasini settings.py da sozlash muhim.
# ---------------------------------------------------------
logger = logging.getLogger(__name__)  # __name__ modul nomi bilan log yozadi



class TeacherListAPIView(ListAPIView):
    """ O'qituvchilar ro'yxatini chiqaruvchi API """

    permission_classes = [permissions.AllowAny]
    serializer_class = TeacherListSerializer
    authentication_classes = AnonRateThrottle

    queryset = Teacher.objects.select_related( # modeldagi ForeginKey lar ni olish uchun
        "user", "science"
    ).prefetch_related( # Teacher, modeli ForeginKey bo'lib ulangan model obyektlarini olish uchun  
        "teacher_group",
        "teacher_certificates",
        "teacher_sms"
    ).all()


    # ---------- FILTR settings ----------
    filter_backends = [
        DjangoFilterBackend,   # ?science=math&gender=male ...
        SearchFilter,          # ?search=ali yoki ?search=ali karimov
        OrderingFilter,        # ?ordering=experience yoki -experience
    ]


    # ---------- FILTER ----------
    filterset_class = TeacherFilter


    # ---------- ORDERING ----------
    ordering_fields = ["experience", "created_at", "date_of_bith", "start_time"]
    ordering = ["-experience"]  # default tartib: eng tajribali o'qituvchilar avval


    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get("search")

        if search: # search uchun maxsus funksiya 
            parts = search.split()

            q = Q()
            for part in parts:
                q |= Q(user__first_name__icontains=part)
                q |= Q(user__last_name__icontains=part)
                q |= Q(science__name__icontains=part)
                q |= Q(user__address__icontains=part)

                # Telefonlar (faqat agar CharField bo'lsa)
                q |= Q(user__phone1__icontains=part)
                q |= Q(user__phone2__icontains=part)

                # Passport (ko'pincha string bo'ladi)
                q |= Q(user__passport__icontains=part)
                q |= Q(dagree__icontains=part)

                # Agar faqat raqam bo'lsa → experience
                if part.isdigit():
                    q |= Q(experience=int(part))

            queryset = queryset.filter(q)

        return queryset




class TeacherDetailAPIView(APIView):
    """
    GET /api/teachers/<slug>/

    Izoh:
    - Detail view faqat o'qish uchun (GET).
    - select_related + prefetch_related bilan optimallashtirilgan queryset ishlatiladi.
    """

    permission_classes = [permissions.AllowAny]  # hamma ko'ra oladi, xohlasangiz o'zgartiring

    def get(self, request, slug):
        """
        GET metod:
        - get_object_or_404 orqali slug bo'yicha Teacher topiladi.
        - agar topilmasa 404 qaytaradi.
        - topilgach, serializer orqali formatlab Response qaytaradi.
        """

        # 1) Log: detail endpoint chaqirildi deb yozamiz
        logger.info(f"Teacher detail API called | slug={slug}")

        # 2) get_object_or_404 bilan obyektni olish:
        #    - select_related('user','science') bilan birga olish — DBga JOIN qiladi
        #    - prefetch_related(...) orqali reverse munosabatlarni oldindan yuklaymiz
        teacher = get_object_or_404(
            Teacher.objects.select_related("user", "science").prefetch_related(
                "teacher_group", "teacher_certificates", "teacher_sms"
            ),
            slug=slug
        )

        # 3) Serializer: bitta obyekt uchun many=False (default)
        serializer = TeacherDetailSerializer(teacher, context={"request": request})

        # 4) Response: serialized data va 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================================================
# 3) TeacherCreateAPIView
#    - yangi o'qituvchi (+nested user creation agar serializer shunday yozilgan bo'lsa)
# =========================================================
# class TeacherCreateAPIView(APIView):
#     """
#     POST /api/teachers/

#     Izoh:
#     - Bu view yangi Teacher yaratish uchun ishlatiladi.
#     - TeacherCreateUpdateSerializer ichida user create logikasi bo'lishi mumkin.
#     """

#     permission_classes = [permissions.IsAuthenticated]  # faqat autentifikatsiyalangan foydalanuvchilar

#     def post(self, request):
#         """
#         POST metod:
#         - request.data ni serializerga beramiz
#         - serializer.is_valid(raise_exception=True) qo'yilsa, xatolar avtomatik 400 qaytadi
#         - serializer.save() orqali model va nested user yaratiladi
#         """

#         # 1) Log: create chaqirildi
#         logger.info("Teacher CREATE API called")

#         # 2) Serializer yaratish: kiruvchi ma'lumotlarni tekshirish uchun
#         serializer = TeacherCreateUpdateSerializer(data=request.data, context={"request": request})

#         # 3) Validatsiya: raise_exception=True bo'lsa, DRF avtomatik 400 qaytaradi va exceptionni ushlab qoladi.
#         if serializer.is_valid(raise_exception=False):
#             # 4) Agar valid bo'lsa saqlashni urinib ko'ramiz (nested create ichida transaction bo'lishi kerak)
#             try:
#                 teacher = serializer.save()  # serializer ichida create() metod batafsil yozilgan bo'lishi kerak
#             except Exception as e:
#                 # Agar save paytida xato bo'lsa, log qilamiz va 500 qaytaramiz
#                 logger.error(f"Error while saving teacher: {e}", exc_info=True)
#                 return Response({"detail": "O'qtuvchi yaratishda ichki xato yuz berdi."},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             # 5) Muvaffaqiyat logi va response
#             logger.info(f"Teacher created: {teacher.slug} (user: {teacher.user.get_full_name()})")
#             return Response({"detail": "O'qtuvchi muvaffaqiyatli yaratildi."}, status=status.HTTP_201_CREATED)

#         # Agar validatsiya xatosi bo'lsa, serializer.errors dict qaytariladi
#         # Note: agar raise_exception=True ishlatilsa shu qator keraksiz
#         logger.warning(f"Teacher create validation failed: {serializer.errors}")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# 4) TeacherUpdateAPIView
#    - PUT (to'liq yangilash) va PATCH (qisman yangilash)
# =========================================================
# class TeacherUpdateAPIView(APIView):
#     """
#     PUT /api/teachers/<slug>/
#     PATCH /api/teachers/<slug>/

#     Izoh:
#     - PUT to'liq yangilash deb qaraladi (partial=False)
#     - PATCH qisman yangilash uchun (partial=True)
#     - Serializer ichida user update uchun ham logika bo'lishi kerak
#     """

#     permission_classes = [permissions.IsAuthenticated]  # faqat autentifikatsiyalangan foydalanuvchilar

#     def get_object(self, slug):
#         """
#         Helper metod:
#         - get_object_or_404 chaqiradi va Teacher obyektini qaytaradi.
#         - view ichidagi PUT/PATCH da DRY uchun ishlatiladi.
#         """
#         return get_object_or_404(Teacher.objects.select_related("user", "science").prefetch_related(
#             "teacher_group", "teacher_certificates", "teacher_sms"
#         ), slug=slug)

#     def put(self, request, slug):
#         """
#         PUT — to'liq yangilash.
#         - partial=False (ya'ni barcha required maydonlar berilishi shart).
#         """
#         logger.info(f"Teacher UPDATE (PUT) called | slug={slug}")

#         teacher = self.get_object(slug)  # obyektni olish

#         # Serializerni yaratamiz: instance va yangi data bilan
#         serializer = TeacherCreateUpdateSerializer(instance=teacher, data=request.data, partial=False,
#                                                    context={"request": request})

#         # Validatsiya va saqlash
#         if serializer.is_valid(raise_exception=False):
#             try:
#                 serializer.save()  # serializer.update() yoki nested user update ishlaydi
#             except Exception as e:
#                 logger.error(f"Error updating teacher (PUT): {e}", exc_info=True)
#                 return Response({"detail": "Yangilashda ichki xato yuz berdi."},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             logger.info(f"Teacher updated (PUT): {slug}")
#             return Response({"detail": "O'qtuvchi to'liq yangilandi."}, status=status.HTTP_200_OK)

#         # Validatsiya xatolari bo'lsa
#         logger.warning(f"Teacher update (PUT) validation failed: {serializer.errors}")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, slug):
#         """
#         PATCH — qisman yangilash.
#         - partial=True (faqat berilgan maydonlar yangilanadi).
#         """
#         logger.info(f"Teacher UPDATE (PATCH) called | slug={slug}")

#         teacher = self.get_object(slug)

#         serializer = TeacherCreateUpdateSerializer(instance=teacher, data=request.data, partial=True,
#                                                    context={"request": request})

#         if serializer.is_valid(raise_exception=False):
#             try:
#                 serializer.save()
#             except Exception as e:
#                 logger.error(f"Error updating teacher (PATCH): {e}", exc_info=True)
#                 return Response({"detail": "Qisman yangilashda ichki xato yuz berdi."},
#                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#             logger.info(f"Teacher updated (PATCH): {slug}")
#             return Response({"detail": "O'qtuvchi qisman yangilandi."}, status=status.HTTP_200_OK)

#         logger.warning(f"Teacher update (PATCH) validation failed: {serializer.errors}")
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# 5) TeacherDeleteAPIView
#    - o'qituvchini o'chirish (DELETE)
# =========================================================
# class TeacherDeleteAPIView(APIView):
#     """
#     DELETE /api/teachers/<slug>/

#     Izoh:
#     - Teacher ni o'chirish CASCADE bilan bog'langan userni ham o'chirishi mumkin
#       (modelingizdagi on_delete parametrlarga qarab).
#     """

#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request, slug):
#         # 1) Log: delete chaqirildi
#         logger.info(f"Teacher DELETE called | slug={slug}")

#         # 2) Teacher obyektini olish yoki 404 qaytarish
#         teacher = get_object_or_404(Teacher, slug=slug)

#         # 3) Obyektni o'chirish
#         try:
#             teacher.delete()  # agar on_delete=CASCADE bo'lsa user ham o'chadi
#         except Exception as e:
#             # Xato bo'lsa log qilamiz va 500 qaytaramiz
#             logger.error(f"Error deleting teacher: {e}", exc_info=True)
#             return Response({"detail": "O'chirishda ichki xato yuz berdi."},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # 4) Muvaffaqiyatli o'chirish logi va 204 NO CONTENT
#         logger.warning(f"Teacher deleted: {slug}")
#         return Response({"detail": "O'qtuvchi muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)







""" --------------------------------------------------------------------------------------------------------------------"""
""" --------------------------------------------  ESKI KODLAR  ---------------------------------------------------------"""
""" --------------------------------------------------------------------------------------------------------------------"""




""" -----------------  O'qtuvchilar uchun CRUD funksiyalari  ------------------- """
# c*-**************************************************************************************************************************************************************************************************************************************************************************************************************


# @throttle_classes([AnonRateThrottle])
# @api_view(["GET"])    
# def teacher_detail(request, slug):
#     """ Birdona o'qtuvchining ma'lumotlarini chiqarish uchun API """

#     teacher = Teacher.objects.filter(slug=slug)
#     serializer = Teacher_Detail_Serializer(teacher, many=True, context={'request':request})
    
#     return Response(serializer.data, status=status.HTTP_200_OK)




# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def teacher_create(request):
#     """ Yangi o'qituvchi va User qo'shish uchun funksiya. """
    
#     print("-------------------------------------------")
    
#     print(request.data)
#     serializer = Teacher_Create_Serializer(data=request.data)
    
#     if serializer.is_valid():
#         serializer.save()        
#         return Response(
#             {'data':f"Yangi o'qtuvchi {serializer.data['user']['first_name']} {serializer.data['user']['last_name']} muvaffaqiyatli qo'shildi"},
#             status=status.HTTP_201_CREATED)
        
#     return Response({'error':f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)









# """ -----------------  Xodimlar uchun CRUD funksiyalari  ------------------- """





