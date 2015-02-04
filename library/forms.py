'''
Created on Jan 12, 2015

@author: josh
'''
from django.forms.models import ModelForm
from library.models import Book, Author, Patron, Checkout
from django import forms

class BookForm(ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all().order_by('last_name', 'first_name'))
    class Meta:
        model = Book
        fields = ['title', 'author']
        
class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
        
class PatronForm(ModelForm):
    class Meta:
        model = Patron
        fields = ['first_name', 'last_name']
        
class CheckoutForm(ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all().order_by('title'))
    patron = forms.ModelChoiceField(queryset=Patron.objects.all().order_by('last_name', 'first_name'))
    
    class Meta:
        model = Checkout
        fields = ['book', 'patron', 'checkout_date', 'checkin_date']