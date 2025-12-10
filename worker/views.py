from rest_framework import status
# from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.throttling import AnonRateThrottle

from django_filters import rest_framework as filters # type: ignore

from .models import Teacher, Worker
from .serializers import TeacherListSerializer, TeacherDetailSerializer



# teacher/views.py

# Django / DRF importlari
import logging
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

# Loyihadagi model va serializer importlari
# Bu qatorlarni loyihangizdagi haqiqiy modul nomlariga moslab o'zgartiring.
from .models import Teacher
from .serializers import TeacherListSerializer, TeacherDetailSerializer
    # TeacherCreateUpdateSerializer,


# ---------------------------------------------------------
# Logger sozlamasi:
# - logger orqali muhim voqealar va xatoliklar filega yoki
#   monitoring tizimiga yozilishi mumkin.
# - productionda LOGGING konfiguratsiyasini settings.py da sozlash muhim.
# ---------------------------------------------------------
logger = logging.getLogger(__name__)  # __name__ modul nomi bilan log yozadi


# =========================================================
# 1) TeacherListAPIView
#    - barcha o'qituvchilar ro'yxatini qaytaradi
#    - select_related va prefetch_related orqali performance optimallashtirilgan
# =========================================================
class TeacherListAPIView(APIView):
    """
    GET /api/teachers/

    Izoh:
    - Bu view barcha o'qituvchilarni qaytaradi.
    - Permission: hozir AllowAny (hamma ko'ra oladi). Agar faqat ichidagi
      foydalanuvchilar ko'rsin desangiz, permissions.IsAuthenticated qo'yasiz.
    """

    # permission_classes atributi klass darajasida ruxsatni belgilaydi.
    permission_classes = [permissions.AllowAny]  # hozir hamma ruxsat oladi

    def get(self, request):
        """
        GET metodi:
        - so'rov parametrlarini o'qiydi (filterlar uchun),
        - querysetni optimallashtirib oladi,
        - serializer orqali JSON formatga o'tkazadi,
        - Response bilan qaytaradi.
        """

        # 1) Log: endpoint chaqirilgani haqida yozib qo'yamiz.
        logger.info("Teacher list API called")

        # 2) Asosiy queryset:
        #    - select_related("user", "science"):
        #       ForeignKey bo'lgan user va science bilan JOIN qilib oladi,
        #       natijada N+1 query muammosi kamayadi.
        #    - prefetch_related(...) (reverse FK yoki many-to-many uchun):
        #       teacher_group, teacher_certificates, teacher_sms kabi
        #       reverse relationshiplarni alohida queryda oldindan yuklaydi.
        queryset = Teacher.objects.select_related("user", "science").prefetch_related(
            "teacher_group",          # teacher -> group (reverse FK) uchun prefetch
            "teacher_certificates",   # teacher -> certificates (reverse FK)
            "teacher_sms"             # teacher -> social media links (reverse FK)
        )

        # 3) Filterlar (soddalashtirilgan):
        #    - request.GET orqali kelgan parametrlarga qarab querysetni filtrlaysiz.
        #    - agar ko'proq murakkab filter kerak bo'lsa, django-filter ishlatish yaxshiroq.
        science = request.GET.get("science")            # masalan ?science=matematika
        gender = request.GET.get("gender")              # masalan ?gender=male
        is_class_leader = request.GET.get("is_class_leader")  # ?is_class_leader=true
        is_mainpage = request.GET.get("is_mainpage")    # ?is_mainpage=1

        # 4) Har bir filter bo'yicha yana querysetni moslab olish:
        #    - science: agar siz science ni FK qilib `slug` bilan so'rasangiz,
        #      queryset.filter(science__slug=science) ishlatiladi.
        if science:
            # Bu yerda biz science ni slug orqali qidiryapmiz.
            queryset = queryset.filter(science__slug=science)

        if gender:
            # user modelida gender maydoni bo'lsa shu orqali filter qilinadi.
            queryset = queryset.filter(user__gender=gender)

        if is_class_leader is not None:
            # is_class_leader boolean bo'lgani uchun "true"/"1" kabi qiymatlarni tekshiramiz
            if is_class_leader.lower() in ("true", "1", "yes"):
                queryset = queryset.filter(is_class_leader=True)
            elif is_class_leader.lower() in ("false", "0", "no"):
                queryset = queryset.filter(is_class_leader=False)

        if is_mainpage is not None:
            # is_mainpage uchun ham xuddi shunday tekshiruv
            if is_mainpage.lower() in ("true", "1", "yes"):
                queryset = queryset.filter(is_mainpage=True)
            elif is_mainpage.lower() in ("false", "0", "no"):
                queryset = queryset.filter(is_mainpage=False)

        # 5) Serializer: queryset ni jarayon uchun serializerga uzatamiz.
        #    - many=True chunki ko'p obyekt qaytadi
        #    - context={'request': request} — serializer ichida .build_absolute_uri
        #      kabi URL yaratish uchun request kerak bo'lishi mumkin.
        serializer = TeacherListSerializer(queryset, many=True, context={"request": request})

        # 6) Natija: serializer.data ni JSON sifatida qaytaramiz.
        #    - status 200 OK
        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================================================
# 2) TeacherDetailAPIView
#    - bitta o'qituvchi haqida batafsil ma'lumot
#    - slug orqali topiladi
# =========================================================
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
class TeacherCreateAPIView(APIView):
    """
    POST /api/teachers/

    Izoh:
    - Bu view yangi Teacher yaratish uchun ishlatiladi.
    - TeacherCreateUpdateSerializer ichida user create logikasi bo'lishi mumkin.
    """

    permission_classes = [permissions.IsAuthenticated]  # faqat autentifikatsiyalangan foydalanuvchilar

    def post(self, request):
        """
        POST metod:
        - request.data ni serializerga beramiz
        - serializer.is_valid(raise_exception=True) qo'yilsa, xatolar avtomatik 400 qaytadi
        - serializer.save() orqali model va nested user yaratiladi
        """

        # 1) Log: create chaqirildi
        logger.info("Teacher CREATE API called")

        # 2) Serializer yaratish: kiruvchi ma'lumotlarni tekshirish uchun
        serializer = TeacherCreateUpdateSerializer(data=request.data, context={"request": request})

        # 3) Validatsiya: raise_exception=True bo'lsa, DRF avtomatik 400 qaytaradi va exceptionni ushlab qoladi.
        if serializer.is_valid(raise_exception=False):
            # 4) Agar valid bo'lsa saqlashni urinib ko'ramiz (nested create ichida transaction bo'lishi kerak)
            try:
                teacher = serializer.save()  # serializer ichida create() metod batafsil yozilgan bo'lishi kerak
            except Exception as e:
                # Agar save paytida xato bo'lsa, log qilamiz va 500 qaytaramiz
                logger.error(f"Error while saving teacher: {e}", exc_info=True)
                return Response({"detail": "O'qtuvchi yaratishda ichki xato yuz berdi."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # 5) Muvaffaqiyat logi va response
            logger.info(f"Teacher created: {teacher.slug} (user: {teacher.user.get_full_name()})")
            return Response({"detail": "O'qtuvchi muvaffaqiyatli yaratildi."}, status=status.HTTP_201_CREATED)

        # Agar validatsiya xatosi bo'lsa, serializer.errors dict qaytariladi
        # Note: agar raise_exception=True ishlatilsa shu qator keraksiz
        logger.warning(f"Teacher create validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# 4) TeacherUpdateAPIView
#    - PUT (to'liq yangilash) va PATCH (qisman yangilash)
# =========================================================
class TeacherUpdateAPIView(APIView):
    """
    PUT /api/teachers/<slug>/
    PATCH /api/teachers/<slug>/

    Izoh:
    - PUT to'liq yangilash deb qaraladi (partial=False)
    - PATCH qisman yangilash uchun (partial=True)
    - Serializer ichida user update uchun ham logika bo'lishi kerak
    """

    permission_classes = [permissions.IsAuthenticated]  # faqat autentifikatsiyalangan foydalanuvchilar

    def get_object(self, slug):
        """
        Helper metod:
        - get_object_or_404 chaqiradi va Teacher obyektini qaytaradi.
        - view ichidagi PUT/PATCH da DRY uchun ishlatiladi.
        """
        return get_object_or_404(Teacher.objects.select_related("user", "science").prefetch_related(
            "teacher_group", "teacher_certificates", "teacher_sms"
        ), slug=slug)

    def put(self, request, slug):
        """
        PUT — to'liq yangilash.
        - partial=False (ya'ni barcha required maydonlar berilishi shart).
        """
        logger.info(f"Teacher UPDATE (PUT) called | slug={slug}")

        teacher = self.get_object(slug)  # obyektni olish

        # Serializerni yaratamiz: instance va yangi data bilan
        serializer = TeacherCreateUpdateSerializer(instance=teacher, data=request.data, partial=False,
                                                   context={"request": request})

        # Validatsiya va saqlash
        if serializer.is_valid(raise_exception=False):
            try:
                serializer.save()  # serializer.update() yoki nested user update ishlaydi
            except Exception as e:
                logger.error(f"Error updating teacher (PUT): {e}", exc_info=True)
                return Response({"detail": "Yangilashda ichki xato yuz berdi."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Teacher updated (PUT): {slug}")
            return Response({"detail": "O'qtuvchi to'liq yangilandi."}, status=status.HTTP_200_OK)

        # Validatsiya xatolari bo'lsa
        logger.warning(f"Teacher update (PUT) validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, slug):
        """
        PATCH — qisman yangilash.
        - partial=True (faqat berilgan maydonlar yangilanadi).
        """
        logger.info(f"Teacher UPDATE (PATCH) called | slug={slug}")

        teacher = self.get_object(slug)

        serializer = TeacherCreateUpdateSerializer(instance=teacher, data=request.data, partial=True,
                                                   context={"request": request})

        if serializer.is_valid(raise_exception=False):
            try:
                serializer.save()
            except Exception as e:
                logger.error(f"Error updating teacher (PATCH): {e}", exc_info=True)
                return Response({"detail": "Qisman yangilashda ichki xato yuz berdi."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info(f"Teacher updated (PATCH): {slug}")
            return Response({"detail": "O'qtuvchi qisman yangilandi."}, status=status.HTTP_200_OK)

        logger.warning(f"Teacher update (PATCH) validation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================================================
# 5) TeacherDeleteAPIView
#    - o'qituvchini o'chirish (DELETE)
# =========================================================
class TeacherDeleteAPIView(APIView):
    """
    DELETE /api/teachers/<slug>/

    Izoh:
    - Teacher ni o'chirish CASCADE bilan bog'langan userni ham o'chirishi mumkin
      (modelingizdagi on_delete parametrlarga qarab).
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, slug):
        # 1) Log: delete chaqirildi
        logger.info(f"Teacher DELETE called | slug={slug}")

        # 2) Teacher obyektini olish yoki 404 qaytarish
        teacher = get_object_or_404(Teacher, slug=slug)

        # 3) Obyektni o'chirish
        try:
            teacher.delete()  # agar on_delete=CASCADE bo'lsa user ham o'chadi
        except Exception as e:
            # Xato bo'lsa log qilamiz va 500 qaytaramiz
            logger.error(f"Error deleting teacher: {e}", exc_info=True)
            return Response({"detail": "O'chirishda ichki xato yuz berdi."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4) Muvaffaqiyatli o'chirish logi va 204 NO CONTENT
        logger.warning(f"Teacher deleted: {slug}")
        return Response({"detail": "O'qtuvchi muvaffaqiyatli o'chirildi."}, status=status.HTTP_204_NO_CONTENT)







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





