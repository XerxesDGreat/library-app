from django.db import models
from datetime import datetime
from django.utils.encoding import smart_text
import re

class LibraryModel(models.Model):
    def form_display_text(self):
        raise NotImplementedError

    @classmethod
    def build_from_value(cls, value):
        raise NotImplementedError

    class Meta:
        abstract = True

class Person(LibraryModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    
    def full_name(self):
        first_name = '' if self.first_name is None else self.first_name
        last_name = '' if self.last_name is None else self.last_name
        return smart_text(" ".join((first_name, last_name)))

    def form_display_text(self):
        return self.full_name()

    @classmethod
    def build_from_value(cls, value):
        pattern = re.compile(r'\s')
        parts = re.split(pattern, value)
        fname = parts[0]
        if len(parts) > 2:
            lname = ' '.join(parts[1:])
        elif len(parts) < 2:
            lname = ''
        else:
            lname = parts[1]
        author = cls(first_name=fname, last_name=lname)
        author.save()
        return author

    
    def __str__(self):
        return self.full_name()
    
    def __unicode__(self):
        return self.full_name()
    
    class Meta:
        abstract = True
    
class Author(Person):
    pass
    #birthday = models.DateField(blank=True, null=True)

class Book(LibraryModel):
    control_number = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=30, blank=True, null=True)
    local_call_number = models.CharField(max_length=40, blank=True, null=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, blank=True, null=True)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    statement_of_responsibility = models.CharField(max_length=100, blank=True, null=True)
    publish_location = models.CharField(max_length=50, blank=True, null=True)
    publish_company = models.CharField(max_length=50, blank=True, null=True)
    publish_date = models.IntegerField(blank=True, null=True)
    extent = models.CharField(max_length=20, blank=True, null=True)
    dimensions = models.CharField(max_length=20, blank=True, null=True)
    series_statement = models.CharField(max_length=50, blank=True, null=True)
    volume_sequential_designation = models.CharField(max_length=10,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    target_audience = models.CharField(max_length=100, blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    series_personal_name = models.ForeignKey(Author, blank=True, null=True, related_name='series_author')
    
    @property
    def published(self):
        return self.publish_date

    def full_title(self):
        by_stmt = self.statement_of_responsibility
        if by_stmt is None:
            by_stmt = 'by %s' % self.author.full_name() if self.author is not None else ''
        subtitle = '' if self.subtitle is None else self.subtitle
        title = self.title
        return smart_text('%s %s %s' % (title, subtitle, by_stmt))

    def form_display_text(self):
        return self.full_title()

    @staticmethod
    def build_from_value(cls, value):
        '''
        We NEED two fields on a book in order to create a new one, and since one of them is itself made up of a value
        requiring two fields, it doesn't make sense to create one here
        '''
        return None
    
    def __str__(self):
        return self.full_title()
    
    def __unicode__(self):
        return self.full_title()
    
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
    checkout_date = models.DateField()
    checkin_date = models.DateField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True, choices=[
        (None, '-- no rating --'),
        (5, 'Loved it'),
        (4, 'Liked it'),
        (3, 'Meh'),
        (2, 'Not good'),
        (1, 'Hated it')
    ])