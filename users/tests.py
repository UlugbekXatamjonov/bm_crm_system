from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.utils import timezone

class CustomUserModelTest(TestCase):

    def setUp(self):
        """
        Testlar uchun namunaviy foydalanuvchini yaratish
        """
        self.user = CustomUser.objects.create_user(
            username="testuser",
            password="testpassword",
            passport="AA1234567",
            date_of_bith="2000-01-01",
            phone1="+998901234567",
            phone2="+998901234568",
            gender="male",
            address="Toshkent, O'zbekiston",
            status=True
        )

    def test_user_creation(self):
        """
        Foydalanuvchi yaratish muvaffaqiyatli o'tganligini tekshirish.
        """
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.passport, "AA1234567")
        self.assertEqual(str(self.user.date_of_bith), "2000-01-01")
        self.assertEqual(self.user.phone1, "+998901234567")
        self.assertEqual(self.user.phone2, "+998901234568")
        self.assertEqual(self.user.gender, "male")
        self.assertEqual(self.user.address, "Toshkent, O'zbekiston")
        self.assertEqual(self.user.status, True)

    def test_user_str_method(self):
        """
        __str__ metodining to'g'ri ishlashini tekshirish.
        """
        self.assertEqual(str(self.user), "testuser")

    
        """
        Telefon raqam validatorining ishlashini tekshirish.
        """
        user = CustomUser.objects.create_user(
            username="testuser2",
            password="testpassword2",
            passport="BB7654321",
            date_of_bith="1995-05-05",
            phone1="12345",  # Noto'g'ri format
            gender="female",
            address="Samarqand, O'zbekiston",
            status=True
        )
        with self.assertRaises(ValidationError):
            user.full_clean()
       
    def test_phone1_number_valid(self):
        """
        Valid telefon raqamlari uchun `phone_regex` validatorini tekshirish.
        """
        user = CustomUser(
            username="testuser1",
            password="testpassword2",
            passport="AA1234568",
            date_of_bith="2000-01-01",
            phone1="+998991234567",
            gender="male",
            address="Tashkent",
            status=True,
        )
        try:
            user.full_clean()  # Validatsiyadan o'tishi kerak
            user.save()
        except ValidationError:
            self.fail("phone1 maydoni uchun validatsiyadan o'tmadi, holbuki bu telefon raqami to'g'ri.")

    def test_phone1_number_invalid(self):
        """
        Noto'g'ri telefon raqamlari uchun `phone_regex` validatorini tekshirish.
        """
        user = CustomUser(
            username="testuser",
            password="testpassword2",
            passport="AA1234567",
            date_of_bith="2000-01-01",
            phone1="998991234567",  # `+` belgisiz noto'g'ri format
            gender="male",
            address="Tashkent",
            status=True,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # Bu yerda validatsiyadan o'tmasligi kerak
    
    def test_phone2_number_valid(self):
        """
        Valid telefon raqamlari uchun `phone2` validatorini tekshirish.
        """
        user = CustomUser(
            username="testuser3",
            password="testpassword2",
            passport="AA1234569",
            date_of_bith="2000-01-01",
            phone1="+998991234567",
            phone2="+998931234567",  # Valid telefon raqami
            gender="male",
            address="Tashkent",
            status=True,
        )
        try:
            user.full_clean()  # Validatsiyadan o'tishi kerak
            user.save()
        except ValidationError:
            self.fail("phone2 maydoni uchun validatsiya o'tmadi, holbuki bu telefon raqami to'g'ri.")

    def test_phone2_number_invalid(self):
        """
        Noto'g'ri telefon raqamlari uchun `phone2` validatorini tekshirish.
        """
        user = CustomUser(
            username="testuser",
            password="testpassword2",
            passport="AA1234567",
            date_of_bith="2000-01-01",
            phone1="+998991234567",
            phone2="931234567",  # `+998` belgisisiz noto'g'ri format
            gender="male",
            address="Tashkent",
            status=True,
        )
        with self.assertRaises(ValidationError):
            user.full_clean()  # Bu yerda validatsiyadan o'tmasligi kerak
    
    def test_default_status(self):
        """
        Default status qiymatining to'g'riligini tekshirish.
        """
        user = CustomUser.objects.create_user(
            username="testuser3",
            password="testpassword3",
            passport="CC0987654",
            date_of_bith="1990-12-12",
            gender="male",
            address="Buxoro, O'zbekiston"
        )
        self.assertEqual(user.status, True)

    def test_auto_now_add_fields(self):
        """
        created_at va updated_at maydonlarining avtomatik ravishda to'ldirilishini tekshirish.
        """
        current_time = timezone.now()

        # created_at va updated_at maydonlarining yaratilgan foydalanuvchi uchun aniq vaqt ichida yaratilganligini tekshirish
        self.assertTrue((current_time - self.user.created_at).total_seconds() < 10)
        self.assertTrue((current_time - self.user.updated_at).total_seconds() < 10)
        
        
        
        
        