from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from library.models import Book
from django.views.generic.base import TemplateResponseMixin

class BookIndexView(generic.ListView):
    template_name = 'books/list.html'
    context_object_name = 'item_list'
    
    def get_queryset(self):
        return Book.objects.order_by('title')

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'library/detail.html'