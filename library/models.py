from django.db import models
from django.db.models.fields import CharField

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    class Meta:
        abstract = True
    
class Author(Person):
    birthday = models.DateField(blank=True, null=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    copyright = models.DateField()
    
class Student(Person):
    pass

class CheckoutRecord(models.Model):
    student = models.ForeignKey(Student)
    book = models.ForeignKey(Book)
    checkout_date = models.DateTimeField()
    checkin_date = models.DateTimeField(blank=True, null=True)