'''
Created on Jan 12, 2015

@author: josh
'''
from django.forms.models import ModelForm
from library.models import Book, Author, Patron, Checkout
from django import forms
from library.widgets import TypeAheadWidget

class BookForm(ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), widget=TypeAheadWidget(model=Author))

    class Meta:
        model = Book
        fields = ['title', 'author', 'control_number', 'publish_date']
        widgets = {
            'publish_date': forms.DateInput(attrs={'class': 'date_picker'}, format='%Y')
        }
        
class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
        
class PatronForm(ModelForm):
    class Meta:
        model = Patron
        fields = ['first_name', 'last_name']
        
class CheckoutForm(ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), widget=TypeAheadWidget(model=Book))
    patron = forms.ModelChoiceField(queryset=Patron.objects.all(), widget=TypeAheadWidget(model=Patron))
    
    class Meta:
        model = Checkout
        fields = ['book', 'patron', 'checkout_date', 'rating']
        widgets = {
            'checkout_date': forms.DateInput(attrs={'class': 'date_picker'}, format='%m/%d/%Y')
        }