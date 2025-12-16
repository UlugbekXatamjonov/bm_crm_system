from rest_framework import serializers

from users.models import CustomUser
from users.serializers import CustomUser_Create_Serializer, CustomUser_List_Serializer, CustomUser_datas_for_Teachers_list_Serializer

from .models import Teacher, Worker, Teacher_Certificate, Teacher_SocialMedia

from django.utils import timezone
from .models import Teacher_Certificate, Teacher_SocialMedia



from rest_framework import serializers
from .models import Teacher_Certificate, Teacher_SocialMedia


class TeacherCertificateSerializer(serializers.ModelSerializer):
    """
    O‘qituvchining sertifikatlari uchun serializer.
    
    Nima uchun kerak?
    - Teacher_Detail_API orqali sertifikatlarni ko‘rsatish uchun
    - CRUD amallarida foydalanish uchun
    """

    class Meta:
        model = Teacher_Certificate
        # Qaysi maydonlar APIda ko‘rinishi kerakligini belgilaymiz
        fields = [
            "id",                # Sertifikatning ID si (frontendga juda kerak bo‘ladi)
            "teacher_name",      # FK — teacher bilan bog‘lanadi
            "name",              # Sertifikat nomi
            "slug",              # Sertifikatning avtomatik slugi
            "photo"              # Sertifikat rasmi
        ]
        read_only_fields = ("slug",)    # slug avtomatik generatsiya bo‘ladi, user o‘zgartira olmaydi


    # ⚠ teacher_name FK bo‘lgani uchun create/update paytida tekshiruvlar qilish mumkin
    def validate_name(self, value):
        """
        Sertifikat nomini validatsiya qilish.
        Masalan:
        - juda qisqa bo‘lsa xatolik chiqaramiz
        - boshqa o‘qituvchida bir xil nomni ruxsat berish mumkin, lekin shu o‘qituvchida takrorlanmasligi kerak
        """
        if len(value) < 3:
            raise serializers.ValidationError("Sertifikat nomi juda qisqa!")
        return value


class TeacherSocialMediaSerializer(serializers.ModelSerializer):
    """
    O‘qituvchining ijtimoiy tarmoqlari uchun serializer.
    """

    class Meta:
        model = Teacher_SocialMedia
        fields = [
            "id",                # Social linkning ID si
            "teacher_name",      # Teacher bilan bog‘langan FK
            "name",              # Tanlangan ijtimoiy tarmoq turi (choices)
            "slug",              # Avtomatik slug
            "url"                # Profil URL manzili
        ]
        read_only_fields = ("slug",)

    def validate_url(self, value):
        """
        URL manzilni validatsiya qilish.
        - manzil 'http' yoki 'https' bilan boshlanishi shart
        - noto‘g‘ri formatda bo‘lsa xato qaytaradi
        """
        if not (value.startswith("http://") or value.startswith("https://")):
            raise serializers.ValidationError("URL manzil 'http://' yoki 'https://' bilan boshlanishi kerak.")
        return value



class TeacherListSerializer(serializers.ModelSerializer):
    """ O'qituvchilar ro'yhati uchun serializer """

    user = CustomUser_List_Serializer(read_only=True) # user ma'lumotlari

    # Fanga doir ma'lumotlar
    science_name = serializers.CharField(source='science.name', read_only=True)
    science_slug = serializers.CharField(source='science.slug', read_only=True)

    # Sinfga doir ma'lumotlar
    group_name_field = serializers.SerializerMethodField()
    group_slug_field = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'user',                 
            'slug',                 
            'photo',
            'science_name',                     
            'science_slug',         
            'is_class_leader',     
            'group_name_field',     
            'group_slug_field',     
        ]
        read_only_fields = ['slug', 'photo', 'science_name', 'science_slug',
                            'group_name_field', 'group_slug_field']

    # ----------------------------
    # DRY helper: guruhni olish uchun ichki funksiya
    # ----------------------------
    def _get_first_group(self, obj):
        """
        Bu private metod teacher ning birinchi tegishli guruhini qaytaradi!
        Izoh:
        - obj.teacher_group prefetched bo'lishi kerak (view da prefetch_related("teacher_group"))
          shunda bu yerda qo'shimcha SQL so'rovi ketmaydi va performance saqlanadi.
        - agar teacher_group bo'sh bo'lsa, None qaytaradi.
        """
        try:
            # teacher_group — siz modelingizda related_name bo'lsa shu nom bilan keladi.
            # Agar related_name boshqacha bo'lsa, shu metodni moslashtiring.
            return obj.teacher_group.first()
        except Exception:
            return None

    def get_group_name_field(self, obj):
        """
        SerializerMethodField uchun getter:
        - birinchi guruhni oladi (agar mavjud bo'lsa) va uning class_name ni qaytaradi.
        - yo'q bo'lsa, None qaytaradi.
        """
        group = self._get_first_group(obj)              # private yordamchi chaqiriladi
        return group.class_name if group is not None else None

    def get_group_slug_field(self, obj):
        """
        SerializerMethodField uchun getter:
        - birinchi guruhni oladi va uning slug ni qaytaradi.
        - yo'q bo'lsa, None qaytaradi.
        """
        group = self._get_first_group(obj)              # bir xil olish logikasi qayta ishlatiladi (DRY)
        return group.slug if group is not None else None



class TeacherDetailSerializer(serializers.ModelSerializer):
    """ O'qtuvchining to'liq ma'lumotlari uchun serializer! """

    user = CustomUser_List_Serializer(read_only=True) # user haqida batafsil ma'lumot (nested serializer orqali)
    # izoh: read_only=True — detailda user ma'lumotlari ko'rsatiladi, lekin shu serializer orqali
    # userni yangilash amalga oshmaydi (alohida user-edit endpoint kerak).

    teacher_certificates = TeacherCertificateSerializer(many=True, read_only=True) # many=True — bir nechta sertifikat qaytishi mumkin.
    teacher_social_links = TeacherCertificateSerializer(many=True, read_only=True)

    # ----------------------------
    # science (ForeignKey) dan tegishli maydonlarni olish:
    # source orqali science.name va science.slug ni olish
    # ----------------------------
    science_name = serializers.CharField(source='science.name', read_only=True)
    science_slug = serializers.CharField(source='science.slug', read_only=True)

    # ----------------------------
    # Guruh nomi va slug uchun SerializerMethodField (xuddi list dagi kabi)
    # ----------------------------
    group_name = serializers.SerializerMethodField()
    group_slug = serializers.SerializerMethodField()

    # ----------------------------
    # Calculated experience — modeldagi start_time hisobiga ko'ra avtomatik hisoblanadi.
    # Agar modelda .experience bazada saqlansa ham, qo'shimcha real-time hisoblamani alohida maydon sifatida qaytaramiz.
    # ----------------------------
    calculated_experience = serializers.SerializerMethodField()

    class Meta:
        """
        Detail serializer uchun Meta:
        - model: Teacher
        - fields: detailda kerakli barcha maydonlar
        - read_only_fields: bir nechta maydon faqat o'qish uchun
        """
        model = Teacher
        fields = [
            "user",                  # nested user obyekti
            "slug",                  # teacher slug (uniqa)
            "photo",                 # rasm
            "passport_photo",        # passport rasmi
            "dagree",                # ma'lumoti / darajasi
            "experience",            # bazadagi experience (agar saqlanadigan bo'lsa)
            "calculated_experience", # start_time asosida real tajriba
            "start_time",            # ish boshlagan sanasi
            "science_name",          # science.name (FK orqali)
            "science_slug",          # science.slug (FK orqali)
            "group_name",            # birinchi guruh nomi
            "group_slug",            # birinchi guruh slugi
            "is_class_leader",       # boolean
            "is_mainpage",           # boolean
            "teacher_certificates",  # nested sertifikatlar
            "teacher_social_links",  # nested social linklar
            "created_at",            # yaratilgan vaqti
            "updated_at",            # oxirgi yangilanish vaqti
        ]
        # read_only_fields - client tomonidan o'zgartirib bo'lmaydigan maydonlar
        read_only_fields = [
            "slug", "user", "science_name", "science_slug",
            "teacher_certificates", "teacher_social_links",
            "created_at", "updated_at", "calculated_experience"
        ]

    # ----------------------------
    # private helper — birinchi guruhni olish (DRY)
    # ----------------------------
    def _get_first_group(self, obj):
        """
        Teacher modelidagi 'teacher_group' related_name orqali birinchi guruhni qaytaradi.
        Izoh: viewda prefetch_related('teacher_group') bo'lsa bu yerda qo'shimcha SQL ishlamaydi!
        """
        try:
            return obj.teacher_group.first()
        except Exception:
            return None

    def get_group_name(self, obj):
        """
        Detail uchun group name qaytaradi.
        """
        group = self._get_first_group(obj)
        return group.class_name if group else None

    def get_group_slug(self, obj):
        """
        Detail uchun group slug qaytaradi.
        """
        group = self._get_first_group(obj)
        return group.slug if group else None

    def get_calculated_experience(self, obj):
        """
        start_time maydoni asosida haqiqiy (hozirgi) tajribani yil bazasida hisoblaydi.
        - Agar start_time mavjud bo'lmasa, bazadagi `experience` maydonini qaytaradi.
        - Agar start_time mavjud bo'lsa, hozirgi kundan yilni hisoblaydi va
          agar hali to'liq yil o'tmagan bo'lsa, mos ravishda kamaytiradi.
        - Natija hech qachon manfiy bo'lmaydi (max(..., 0)).
        """
        # agar start_time bo'lmasa, bazadagi maydondan foydalanamiz (agar u mavjud bo'lsa)
        if not getattr(obj, 'start_time', None):
            # obj.experience maydoni modelda mavjud ekanligini taxmin qilamiz
            return getattr(obj, 'experience', 0)

        # bugungi sana
        today = timezone.now().date()
        start = obj.start_time

        # yil farqi
        years = today.year - start.year

        # agar hozirgi oy-kun start oy-kundan oldin bo'lsa, to'liq yil o'tmagan hisoblanadi
        if (today.month, today.day) < (start.month, start.day):
            years -= 1

        # manfiyga tushmasligi uchun 0 bilan solishtiramiz
        return max(years, 0)


















""" --------------------------------------------------------------------------------------------------------------------"""
""" --------------------------------------------  ESKI KODLAR  ---------------------------------------------------------"""
""" --------------------------------------------------------------------------------------------------------------------"""




# class TeacherCertificateSerializer(serializers.ModelSerializer):
#     """ O‘qituvchining sertifikatlari uchun serializer."""

#     class Meta:
#         model = Teacher_Certificate
#         fields = [
#             "id",                
#             "teacher_name",       
#             "name",              
#             "slug",              
#             "photo"              
#         ]
#         read_only_fields = ("slug",)    # slug avtomatik generatsiya bo‘ladi, user o‘zgartira olmaydi


#     # ⚠ teacher_name FK bo‘lgani uchun create/update paytida tekshiruvlar qilish mumkin
#     def validate_name(self, value):
#         """
#         Sertifikat nomini validatsiya qilish.
#         Masalan:
#         - juda qisqa bo‘lsa xatolik chiqaramiz
#         - boshqa o‘qituvchida bir xil nomni ruxsat berish mumkin, lekin shu o‘qituvchida takrorlanmasligi kerak
#         """
#         if len(value) < 3:
#             raise serializers.ValidationError("Sertifikat nomi juda qisqa!")
#         return value



# class TeacherSocialMediaSerializer(serializers.ModelSerializer):
#     """ O‘qituvchining ijtimoiy tarmoqlari uchun serializer."""

#     class Meta:
#         model = Teacher_SocialMedia
#         fields = [
#             "id",                
#             "teacher_name",      
#             "name",               
#             "slug",              
#             "url"                 
#         ]
#         read_only_fields = ("slug",)

#     def validate_url(self, value):
#         """
#         URL manzilni validatsiya qilish.
#         - manzil 'http' yoki 'https' bilan boshlanishi shart
#         - noto‘g‘ri formatda bo‘lsa xato qaytaradi
#         """
#         if not (value.startswith("http://") or value.startswith("https://")):
#             raise serializers.ValidationError("URL manzil 'http://' yoki 'https://' bilan boshlanishi kerak.")
#         return value



# Quyidagi model va serializerlarni loyihangizdan import qiling:
# from .models import Teacher  # sizning Teacher modeli (science = ForeignKey)
# from users.serializers import CustomUser_List_Serializer  # user haqida to'liq ma'lumot qaytaruvchi serializer
# from .models import TeacherCertificate, TeacherSocialMedia  # agar nomlar boshqacha bo'lsa moslang
# from .serializers import Teacher_Certificate_Serializer, Teacher_SocialMediaSerializer

# ========================================================================
# 1) TeacherListSerializer
#    - ro'yxat (list) uchun yengil va tezkor serializatsiya
#    - select_related / prefetch_related yordamida viewda optimallashtirish kutiladi
# ========================================================================

# class TeacherListSerializer(serializers.ModelSerializer):
#     """
#     O'qituvchilar ro'yhati uchun serializer!
#     Har bir maydon ostida nima qilinayotgani qat'iy izohlangan.
#     """

#     # ------------------------------------------------------------
#     # Biz user haqidagi ustunlarni nested serializer orqali qaytaramiz.
#     # Bu yerda 'CustomUser_List_Serializer' siz yaratgan va user haqida
#     # kerakli maydonlarni qaytaruvchi serializer bo'lishi kerak.
#     # ------------------------------------------------------------
#     user = CustomUser_List_Serializer(read_only=True)
#     # izoh: read_only=True — list endpoint orqali user ma'lumotlarini o'qish uchun ishlatiladi,
#     # yozish (create/update) bu serializer orqali amalga oshirilmaydi.

#     # ------------------------------------------------------------
#     # science — Teacher modelida ForeignKey ekan, uning ichidagi
#     # name va slug kabi maydonlarni to'g'ridan-to'g'ri manba orqali olish:
#     # source='science.name' va source='science.slug' ishlatiladi.
#     # ------------------------------------------------------------
#     science_name = serializers.CharField(source='science.name', read_only=True)
#     # izoh: source='science.name' — Teacher.objects.select_related('science') qilinganda
#     # qo'shimcha query jo'natmaydi va science.name ni qaytaradi.

#     science_slug = serializers.CharField(source='science.slug', read_only=True)
#     # izoh: agar science modelida slug maydon bo'lsa, uni shu tarzda qaytaramiz.

#     # ------------------------------------------------------------
#     # Guruh nomi va slug uchun SerializerMethodField ishlatamiz,
#     # chunki teacher->group munosabati 1-to-ko'p bo'lishi mumkin va
#     # biz birinchi (yoki logikaga mos) guruhni qaytarmoqchimiz.
#     # ------------------------------------------------------------
#     group_name_field = serializers.SerializerMethodField()
#     group_slug_field = serializers.SerializerMethodField()

#     class Meta:
#         """
#         Meta ichida quyidagilarni belgilaymiz:
#         - model: asosiy model (Teacher)
#         - fields: ro'yxatga qaytariladigan maydonlar tartibi
#         - read_only_fields: ro'yxat uchun o'zgarmas maydonlar
#         """
#         model = Teacher
#         fields = [
#             'user',                # nested user ma'lumotlari
#             'slug',                # teacher slug (uniqsiz bo'lmasligi kerak emas)
#             'photo',               # profil rasmi (url qaytariladi)
#             'science_name',        # science modelidan name
#             'science_slug',        # science modelidan slug
#             'is_class_leader',     # boolean
#             'group_name_field',    # SerializerMethodField orqali olingan group name
#             'group_slug_field',    # SerializerMethodField orqali olingan group slug
#         ]
#         read_only_fields = ['slug', 'photo', 'science_name', 'science_slug',
#                             'group_name_field', 'group_slug_field']

#     # ----------------------------
#     # DRY helper: guruhni olish uchun ichki funksiya
#     # ----------------------------
#     def _get_first_group(self, obj):
#         """
#         Bu private metod teacher ning birinchi tegishli guruhini qaytaradi!
#         Izoh:
#         - obj.teacher_group prefetched bo'lishi kerak (view da prefetch_related("teacher_group"))
#           shunda bu yerda qo'shimcha SQL so'rovi ketmaydi va performance saqlanadi.
#         - agar teacher_group bo'sh bo'lsa, None qaytaradi.
#         """
#         try:
#             # teacher_group — siz modelingizda related_name bo'lsa shu nom bilan keladi.
#             # Agar related_name boshqacha bo'lsa, shu metodni moslashtiring.
#             return obj.teacher_group.first()
#         except Exception:
#             # Agar relation mavjud bo'lmasa yoki nom boshqacha bo'lsa None qaytaramiz.
#             return None

#     def get_group_name_field(self, obj):
#         """
#         SerializerMethodField uchun getter:
#         - birinchi guruhni oladi (agar mavjud bo'lsa) va uning class_name ni qaytaradi.
#         - yo'q bo'lsa, None qaytaradi.
#         """
#         group = self._get_first_group(obj)              # private yordamchi chaqiriladi
#         return group.class_name if group is not None else None

#     def get_group_slug_field(self, obj):
#         """
#         SerializerMethodField uchun getter:
#         - birinchi guruhni oladi va uning slug ni qaytaradi.
#         - yo'q bo'lsa, None qaytaradi.
#         """
#         group = self._get_first_group(obj)              # bir xil olish logikasi qayta ishlatiladi (DRY)
#         return group.slug if group is not None else None


# ========================================================================
# 2) TeacherDetailSerializer
#    - batafsil ko'rinish uchun serializer
#    - nested sertifikatlar va social linklar qo'shiladi
#    - science (FK) dan name va slug olinadi
#    - experience: bazadagi saqlangan maydon + hisoblangan variant (calculated) mavjud bo'lishi mumkin
# ========================================================================

# class TeacherDetailSerializer(serializers.ModelSerializer):
#     """
#     Birdona o'qtuvchining to'liq ma'lumotlari uchun serializer!
#     Har bir qatorda nima qilinganligi to'liq tushuntirilgan.
#     """

#     # ----------------------------
#     # user haqida batafsil ma'lumot (nested serializer orqali)
#     # ----------------------------
#     user = CustomUser_List_Serializer(read_only=True)
#     # izoh: read_only=True — detailda user ma'lumotlari ko'rsatiladi, lekin shu serializer orqali
#     # userni yangilash amalga oshmaydi (alohida user-edit endpoint kerak).

#     # ----------------------------
#     # Sertifikatlar va social linklarni nested serializerlarda qaytarish
#     # teacher.certificates va teacher.social_links (related_name) orqali olamiz.
#     # ----------------------------
#     teacher_certificates = TeacherCertificateSerializer(many=True, read_only=True)
#     # izoh: many=True — bir nechta sertifikat qaytishi mumkin.

#     teacher_social_links = TeacherSocialMediaSerializer(many=True, read_only=True)
#     # izoh: related_name modelda 'social_links' deb berilgan bo'lsa shu nomdan olinadi.

#     # ----------------------------
#     # science (ForeignKey) dan tegishli maydonlarni olish:
#     # source orqali science.name va science.slug ni olish
#     # ----------------------------
#     science_name = serializers.CharField(source='science.name', read_only=True)
#     science_slug = serializers.CharField(source='science.slug', read_only=True)

#     # ----------------------------
#     # Guruh nomi va slug uchun SerializerMethodField (xuddi list dagi kabi) 
#     # ----------------------------
#     group_name = serializers.SerializerMethodField()
#     group_slug = serializers.SerializerMethodField()

#     # ----------------------------
#     # Calculated experience — modeldagi start_time hisobiga ko'ra avtomatik hisoblanadi.
#     # Agar modelda .experience bazada saqlansa ham, qo'shimcha real-time hisoblamani alohida maydon sifatida qaytaramiz.
#     # ----------------------------
#     calculated_experience = serializers.SerializerMethodField()

#     class Meta:
#         """
#         Detail serializer uchun Meta:
#         - model: Teacher
#         - fields: detailda kerakli barcha maydonlar
#         - read_only_fields: bir nechta maydon faqat o'qish uchun
#         """
#         model = Teacher
#         fields = [
#             "user",                  # nested user obyekti
#             "slug",                  # teacher slug (uniqa)
#             "photo",                 # rasm
#             "passport_photo",        # passport rasmi
#             "dagree",                # ma'lumoti / darajasi
#             "experience",            # bazadagi experience (agar saqlanadigan bo'lsa)
#             "calculated_experience", # start_time asosida real tajriba
#             "start_time",            # ish boshlagan sanasi
#             "science_name",          # science.name (FK orqali)
#             "science_slug",          # science.slug (FK orqali)
#             "group_name",            # birinchi guruh nomi
#             "group_slug",            # birinchi guruh slugi
#             "is_class_leader",       # boolean
#             "is_mainpage",           # boolean
#             "teacher_certificates",  # nested sertifikatlar
#             "teacher_social_links",  # nested social linklar
#             "created_at",            # yaratilgan vaqti
#             "updated_at",            # oxirgi yangilanish vaqti
#         ]
#         # read_only_fields - client tomonidan o'zgartirib bo'lmaydigan maydonlar
#         read_only_fields = [
#             "slug", "user", "science_name", "science_slug",
#             "teacher_certificates", "teacher_social_links",
#             "created_at", "updated_at", "calculated_experience"
#         ]

#     # ----------------------------
#     # private helper — birinchi guruhni olish (DRY)
#     # ----------------------------
#     def _get_first_group(self, obj):
#         """
#         Teacher modelidagi 'teacher_group' related_name orqali birinchi guruhni qaytaradi.
#         Izoh: viewda prefetch_related('teacher_group') bo'lsa bu yerda qo'shimcha SQL ishlamaydi!
#         """
#         try:
#             return obj.teacher_group.first()
#         except Exception:
#             return None

#     def get_group_name(self, obj):
#         """
#         Detail uchun group name qaytaradi.
#         """
#         group = self._get_first_group(obj)
#         return group.class_name if group else None

#     def get_group_slug(self, obj):
#         """
#         Detail uchun group slug qaytaradi.
#         """
#         group = self._get_first_group(obj)
#         return group.slug if group else None

#     def get_calculated_experience(self, obj):
#         """
#         start_time maydoni asosida haqiqiy (hozirgi) tajribani yil bazasida hisoblaydi.
#         - Agar start_time mavjud bo'lmasa, bazadagi `experience` maydonini qaytaradi.
#         - Agar start_time mavjud bo'lsa, hozirgi kundan yilni hisoblaydi va
#           agar hali to'liq yil o'tmagan bo'lsa, mos ravishda kamaytiradi.
#         - Natija hech qachon manfiy bo'lmaydi (max(..., 0)).
#         """
#         # agar start_time bo'lmasa, bazadagi maydondan foydalanamiz (agar u mavjud bo'lsa)
#         if not getattr(obj, 'start_time', None):
#             # obj.experience maydoni modelda mavjud ekanligini taxmin qilamiz
#             return getattr(obj, 'experience', 0)

#         # bugungi sana
#         today = timezone.now().date()
#         start = obj.start_time

#         # yil farqi
#         years = today.year - start.year

#         # agar hozirgi oy-kun start oy-kundan oldin bo'lsa, to'liq yil o'tmagan hisoblanadi
#         if (today.month, today.day) < (start.month, start.day):
#             years -= 1

#         # manfiyga tushmasligi uchun 0 bilan solishtiramiz
#         return max(years, 0)







































""" --------------------- ❗❗❗ Eski kodlar ❗❗❗ ---------------------  """

""" --------------------- Teacher Section ---------------------  """
# class Teacher_Certificate_Serializer(serializers.ModelSerializer):
#     """ O'qtuvchining sertifikatlari uchun serializer """

#     class Meta:
#         model = Teacher_Certificate
#         fields = ['name', 'slug']


# class Teacher_SM_Serializer(serializers.ModelSerializer):
#     """ O'qtuvchining sertifikatlari uchun serializer """

#     class Meta:
#         model = Teacher_SocialMedia
#         fields = ['name', 'slug']


# class Teacher_Create_Serializer(serializers.ModelSerializer):
#     """
#     O'qtuvchi qo'shish uchun serializer.
#     CustomUserSerializer() orqali bir vaqtning o'zida yangi User ham qo'shilib, u asosida Teacher obyetki ham qo'shiladi
#     """
#     user = CustomUser_Create_Serializer()  # Yangi user qo'shish uchun CustomUser serializerini ishlatamiz

#     class Meta:
#         model = Teacher
#         fields = ['user', 'slug', 'photo', 'passport_photo', 'science', 'dagree', 'experience', 
#                     'start_time', 'is_class_leader', 'is_mainpage']


#     def create(self, validated_data):
#         """
#         Yangi o'qituvchi yaratishda, bir vaqtning o'zida CustomUser ni ham yaratish.
#         """
#         user_data = validated_data.pop('user')  # 'user' ma'lumotlarini ajratib olamiz
#         user = CustomUser.objects.create(**user_data)  # CustomUser obyekti yaratamiz
#         teacher = Teacher.objects.create(user=user, **validated_data)  # Teacher obyekti yaratamiz
        
#         return teacher

        
# class Teacher_List_Serializer(serializers.ModelSerializer):
#     """ O'qtuvchilar ro'yhari uchun Serializer """
    
#     user = CustomUser_datas_for_Teachers_list_Serializer()  # User malumotlarini olish uchun ushbu serializerni ishlatamiz 

#     science_name = serializers.CharField(source='science.name')
#     science_slug = serializers.CharField(source='science.slug')
    
#     group_name_field = serializers.SerializerMethodField()
#     group_slug_field = serializers.SerializerMethodField()

#     class Meta:
#         model = Teacher
#         fields = ['user', 'slug', 'photo', 'science_name', 'science_slug', 'is_class_leader', 
#                     'group_name_field', 'group_slug_field']


#     def get_group_name_field(self, obj):
#         """ O'qituvchining guruhining nomini qaytaradi """
        
#         group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
#         if group_instance: # agar o'qtuvchining sinfi bo'lsa
#             return group_instance.class_name # sinfning nomini qaytaramiz
#         else:
#             return None #Aks holda bo'sh qiymat qaytaramiz
    
#     def get_group_slug_field(self, obj):
#         """ O'qituvchining guruhining slugini qaytaradi """
        
#         group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
#         if group_instance: # agar o'qtuvchining sinfi bo'lsa
#             return group_instance.slug # sinfning nomini qaytaramiz
#         else:
#             return None #Aks holda bo'sh qiymat qaytaramiz


# class Teacher_Detail_Serializer(serializers.ModelSerializer):
#     """ Birdona o'qtuvchining ma'lumotlarini chiqarish uchun serializer """

#     user = CustomUser_List_Serializer()
#     teacher_certificates = Teacher_Certificate_Serializer(many=True, read_only=True)
#     # teacher_sms = Teacher_SM_Serializer(many=True, read_only=True)

#     science_name = serializers.CharField(source='science.name')
#     science_slug = serializers.CharField(source='science.slug')
    
#     group_name = serializers.SerializerMethodField()
#     group_slug = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Teacher
#         fields = ["user", "slug", "photo", "passport_photo", "dagree", "experience", "start_time", 
#                     "science_name", "science_slug", "group_name", "group_slug",   
#                     "is_class_leader", "is_mainpage",
#                     "teacher_certificates"
#                 ]

    
#     def get_group_name(self, obj):
#         """ O'qituvchining guruhining nomini qaytaradi """
        
#         group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
#         if group_instance: # agar o'qtuvchining sinfi bo'lsa
#             return group_instance.class_name # sinfning nomini qaytaramiz
#         else:
#             return None #Aks holda bo'sh qiymat qaytaramiz
    
#     def get_group_slug(self, obj):
#         """ O'qituvchining guruhining slugini qaytaradi """
        
#         group_instance = obj.teacher_group.first()  # related_name orqali o'qtuvchining guruhlari ro'yxatidan 1-guruhini olamiz
        
#         if group_instance: # agar o'qtuvchining sinfi bo'lsa
#             return group_instance.slug # sinfning nomini qaytaramiz
#         else:
#             return None #Aks holda bo'sh qiymat qaytaramiz




""" --------------------- Worker Section ---------------------  """
# class WorkerSerializer(serializers.ModelSerializer):
    # """
    # Xodim (Worker) modeliga oid serializer.
    # - Bu serializer Worker modelidagi barcha maydonlarni o'z ichiga oladi.
    # """

    # class Meta:
    #     model = Worker
    #     fields = ['id', 'user', 'photo', 'is_superadmin', 'salary']


