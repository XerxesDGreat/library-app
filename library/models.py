from django.db import models
from datetime import datetime

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    def full_name(self):
        return " ".join((self.first_name, self.last_name))
    
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
    
    class Meta:
        abstract = True
    
class Author(Person):
    pass
    #birthday = models.DateField(blank=True, null=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    published = models.DateField()
    
    def __str__(self):
        return '%s (%s)' % (self.title, datetime.strftime(self.published, "%Y"))
    
class Patron(Person):
    _patron_types = {
        'A': 'Administration',
        'P': 'Parent',
        'S': 'Student',
        'T': 'Teacher'
    }
    
    bar_code = models.CharField(max_length=8, blank=True, null=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    type = models.CharField(max_length=1,choices=[('S', 'Student'), ('P', 'Parent'), ('A', 'Admin'), ('T', 'Teacher')], blank=True, null=True)
    report_to = models.ForeignKey('Patron', limit_choices_to={'is_staff', True}, blank=True, null=True)
    organization = models.CharField(max_length=20, blank=True, null=True)
    department = models.CharField(max_length=20, blank=True, null=True)
    address_1 = models.CharField(max_length=100, blank=True, null=True)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=35, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=6, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)
    parent_info = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    custom_field_1 = models.TextField(blank=True, null=True)
    custom_field_2 = models.TextField(blank=True, null=True)
    custom_field_3 = models.TextField(blank=True, null=True)
    custom_field_4 = models.TextField(blank=True, null=True)
    
    def is_staff(self):
        return self.type in ['A', 'T']

    def is_student(self):
        return self.type == 'S'
    
    def patron_type(self):
        try:
            return self._patron_types[self.type]
        except:
            return 'Other'
            

class Checkout(models.Model):
    patron = models.ForeignKey(Patron)
    book = models.ForeignKey(Book)
    checkout_date = models.DateTimeField()
    checkin_date = models.DateTimeField(blank=True, null=True)
    
class Rating(models.Model):
    patron = models.ForeignKey(Patron)
    book = models.ForeignKey(Book)
    rating = models.IntegerField()
    comments = models.TextField(blank=True, null=True)