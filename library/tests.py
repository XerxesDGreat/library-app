from django.test import TestCase
from models import Student

class ModelTest(TestCase):
    def test_student_full_name(self):
        a = Student(first_name='asdf', last_name='qwer')
        self.assertEqual('asdf qwer', a.full_name())