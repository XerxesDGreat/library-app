from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    
    def full_name(self):
        return " ".join((self.first_name, self.last_name))
    
    class Meta:
        abstract = True
    
class Author(Person):
    pass
    #birthday = models.DateField(blank=True, null=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author)
    published = models.DateField()
    
class Student(Person):
    pass

class Checkout(models.Model):
    student = models.ForeignKey(Student)
    book = models.ForeignKey(Book)
    checkout_date = models.DateTimeField()
    checkin_date = models.DateTimeField(blank=True, null=True)
    
class Rating(models.Model):
    student = models.ForeignKey(Student)
    book = models.ForeignKey(Book)
    rating = models.IntegerField()
    comments = models.TextField()