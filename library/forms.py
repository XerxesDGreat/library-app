'''
Created on Jan 12, 2015

@author: josh
'''
from django.forms.models import ModelForm
from library.models import Book, Author, Student, Checkout
from django import forms

class BookForm(ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all().order_by('last_name', 'first_name'))
    class Meta:
        model = Book
        fields = ['title', 'author', 'published']
        
class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
        
class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name']
        
class CheckoutForm(ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all().order_by('title', 'published'))
    student = forms.ModelChoiceField(queryset=Student.objects.all().order_by('last_name', 'first_name', 'grade'))
    
    class Meta:
        model = Checkout
        fields = ['book', 'student', 'checkout_date', 'checkin_date']