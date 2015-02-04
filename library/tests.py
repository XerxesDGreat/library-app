from django.test import TestCase
from models import Patron, Book, Author

class PatronTest(TestCase):
    def test_student_full_name(self):
        a = Patron(first_name='asdf', last_name='qwer')
        self.assertEqual('asdf qwer', a.full_name())
        
    def test_is_staff(self):
        for t, is_staff in [('S', False), ('P', False), ('A', True), ('T', True)]:
            a = Patron(type=t)
            self.assertEqual(is_staff, a.is_staff())
            
class BookTest(TestCase):
    def test_full_title(self):
        a = Author(first_name='Steven', last_name='King')
        b = Book(title='It', author=a)
        self.assertEqual('It  Steven King', b.full_title())