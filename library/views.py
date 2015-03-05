from django.shortcuts import get_object_or_404, render_to_response
from django.views import generic
import json

from library.models import Author, Book, Patron, Checkout
from library_app.utils import reverse
from library.forms import BookForm, CheckoutForm#, AuthorForm, PatronForm
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import HttpResponse
from django.db.models import Q
from operator import itemgetter


def _person_search(request, cls):
    term = request.GET.get('term')
    matches = []
    if term is not None:
        search = Q(first_name__icontains=term) | Q(last_name__icontains=term)
        matches = [{'label': a.full_name(), 'value': a.full_name(), 'id': a.id} for a in cls.objects.filter(search).order_by('last_name')]
    return HttpResponse(json.dumps(matches), content_type='application/json')

#########################################################
## Authors
class AuthorIndexView(generic.ListView):
    template_name='authors/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        context['added_id'] = self.request.GET.get('added_id')
        context['return_url'] = self.request.GET.get('return_url')
        return context
    
    def get_queryset(self):
        return Author.objects.order_by('last_name').order_by('first_name')
    
class AuthorDetailView(generic.DetailView):
    model = Author
    template = 'authors/form.html'
    
class AuthorCreateView(generic.CreateView):
    model = Author
    fields = ['first_name', 'last_name']
    template = 'authors/form.html'
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['author'] = self.object
        return context_data
    
    def get_success_url(self):
        return reverse('library:author_index', query_args={'added_id': self.object.id})

def author_search(request):
    return _person_search(request, Author)

#########################################################
## Books
class BookIndexView(generic.ListView):
    template_name = 'books/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        context['added_id'] = self.request.GET.get('added_id')
        context['search_term'] = self.request.GET.get('q')
        context['carryover_query_params'] = self.request.GET.dict()
        context['patron_id'] = self.request.GET.get('patron_id')
        context['return_url'] = self.request.GET.get('return_url')
        return context
    
    def get_queryset(self):
        search_term = self.request.GET.get('q')
        queryset = Book.objects.all().order_by('title')
        if search_term is not None:
            queryset = queryset.filter(title__icontains=search_term)
        return queryset

class BookUpdateView(generic.UpdateView):
    form_class = BookForm
    model = Book
    fields = ['title', 'author', 'published']
    template_name = 'books/form.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookUpdateView, self).get_context_data(**kwargs)
        context['form_action'] = 'add' if self.object is None else 'edit'
        return context
    
    def get_success_url(self):
        query_args = None
        if self.object:
            query_args = {'edited': self.object.id}
            
        return reverse('library:book_index', query_args=query_args)

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        recommended_books = {}
        be = Checkout.objects.filter(book__id=self.object.id)
        for book_entry in be:
            se = Checkout.objects.filter(patron__id=book_entry.patron.id)
            for patron_entry in se:
                if patron_entry.book.id == self.object.id:
                    continue
                try:
                    weighted_amount = 1 if book_entry.rating is None else book_entry.rating - 1.5
                    recommended_books[patron_entry.book]['count'] += weighted_amount
                except:
                    recommended_books[patron_entry.book] = {'book': patron_entry.book, 'count': 1}
        context['recommended_book_list'] = [y[1] for y in sorted(recommended_books.items(), key=lambda x: x[1]['count'], reverse=True)]
        return context

class BookCreateView(generic.CreateView):
    model = Book
    form_class = BookForm
    template_name = 'books/form.html'
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['book'] = self.object
        try:
            context_data['author'] = Author.objects.get(pk=self.request.GET.get('author_id'))
        except:
            context_data['author'] = None
        return context_data
    
    def get_success_url(self):
        return reverse('library:book_index', query_args={'added_id': self.object.id})
    
def book_title_search(request):
    query_val = request.GET.get('term')
    matches = []
    if query_val is not None:
        matches = [{'label': b.title, 'value': b.title, 'id': b.id} for b in Book.objects.filter(title__icontains=query_val).order_by('title')]
    return HttpResponse(json.dumps(matches), content_type='application/json')
    
#########################################################
## Patrons
class PatronIndexView(generic.ListView):
    template_name = 'patrons/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        context['added_id'] = self.request.GET.get('added_id')
        context['search_term'] = self.request.GET.get('q')
        context['carryover_query_params'] = self.request.GET.dict()
        context['book_id'] = self.request.GET.get('book_id')
        context['return_url'] = self.request.GET.get('return_url')
        return context
    
    def get_queryset(self):
        search_term = self.request.GET.get('q')
        queryset = Patron.objects.all().order_by('title')
        if search_term is not None:
            queryset = queryset.filter(Q(first_name__icontains=search_term) | Q(last_name__icontains=search_term))
        return queryset.order_by('type', 'department', 'last_name', 'first_name')

class PatronDetailView(generic.DetailView):
    model = Patron
    template_name = 'patrons/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PatronDetailView, self).get_context_data(**kwargs)
        context['circ_history'] = Checkout.objects.filter(patron__id=self.object.id)
        book_co_count = {}
        for book_entry in context['circ_history']:
            for patron_entry in Checkout.objects.filter(book__id=book_entry.book.id):
                if patron_entry.patron.id == self.object.id:
                    continue
                try:
                    amount = 1 if book_entry.rating is None else book_entry.rating - 1.5
                    book_co_count[patron_entry.book]['count'] += amount
                except Exception as e:
                    book_co_count[patron_entry.book] = {'book': patron_entry.book, 'count': 1}

        sorted_books = [bc[1] for bc in (sorted(book_co_count.items(), key=lambda book_count_entry: book_count_entry[1]['count']))]
        context['book_recommendations'] = sorted_books
        return context

class PatronUpdateView(generic.UpdateView):
    #form_class = PatronForm
    model = Patron
    fields = ['first_name', 'last_name', 'grade']
    template_name = 'patrons/form.html'
    
    def get_context_data(self, **kwargs):
        context = super(PatronUpdateView, self).get_context_data(**kwargs)
        #context['form_action'] = 'add' if self.object is None else 'edit'
        return context
    
    def get_success_url(self):
        query_args = None
        if self.object:
            query_args = {'edited': self.object.id}
            
        return reverse('library:patron_index', query_args=query_args)

class PatronCreateView(generic.CreateView):
    model = Patron
    fields = ['first_name', 'last_name', 'grade']
    template_name = 'patrons/form.html'
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['patron'] = self.object
        return context_data
    
    def get_success_url(self):
        return reverse('library:patron_index', query_args={'added_id': self.object.id})
    
    
def patron_search(request):
    return _person_search(request, Patron)
    
#########################################################
## Circulation
class CirculationIndexView(generic.ListView):
    template_name = 'circulation/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    page_title = 'Circulation History'
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        context['page_title'] = self._get_page_title()
        a = context['item_list'][1]
        return context
    
    def _get_page_title(self):
        return self.page_title
    
    def get_queryset(self):
        return Checkout.objects.order_by('-checkout_date', '-checkin_date', 'book__title')

class CirculationDetailView(generic.UpdateView):
    form_class = CheckoutForm
    model = Checkout
    fields = ['checkout_date', 'checkin_date', 'patron', 'book']
    template_name = 'circulation/form.html'
    
    def get_context_data(self, **kwargs):
        context = super(CirculationDetailView, self).get_context_data(**kwargs)
        context['form_action'] = 'add' if self.object is None else 'edit'
        context['selected_book'] = context['checkout'].book
        return context
    
    def get_success_url(self):
        query_args = None
        if self.object:
            query_args = {'edited': self.object.id}
            
        return reverse('library:circulation_index', query_args=query_args)
    
class CirculationCreateView(generic.CreateView):
    model = Checkout
    form_class = CheckoutForm
    template_name = 'circulation/form.html'
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['checkout'] = self.object
        try:
            context_data['selected_book'] = Book.objects.get(pk=self.request.GET.get('book_id'))
        except:
            context_data['selected_book'] = None
        try:
            context_data['selected_patron'] = Patron.objects.get(pk=self.request.GET.get('patron_id'))
        except:
            context_data['selected_patron'] = None
        return context_data
    
    def get_success_url(self):
        return reverse('library:circulation_index', query_args={'added_id': self.object.id})

class CirculationIndexByPatronView(CirculationIndexView):
    patron = None
    
    def get_queryset(self):
        patron = self._get_patron()
        return Checkout.objects.filter(patron_id=patron.id).order_by('-checkout_date')
    
    def _get_page_title(self):
        patron = self._get_patron()
        return '%s for %s' % (self.page_title, patron.full_name())
    
    def _get_patron(self):
        if self.patron is None:
            self.patron = get_object_or_404(Patron, pk=self.kwargs.get('pk'))
        return self.patron

def highest_rated_titles(request, **kwargs):
    checkouts = Checkout.objects.all()
    b = {}
    print 'before loop'
    for c in checkouts:
        try:
            st = b[c.book]
        except:
            st = {
                'title': c.book.title,
                'checkouts': 0,
                'total_rating': None,
                'num_ratings': 0,
                'avg_rating': None
            }
        st['checkouts'] += 1
        if c.rating is not None:
            st['num_ratings'] += 1
            st['total_rating'] = st['total_rating'] + c.rating if st['total_rating'] else float(c.rating)
            st['avg_rating'] = st['total_rating'] / st['num_ratings']

        b[c.book] = st

    print 'after loop'

    sorted_b = sorted(b.values(), key=itemgetter('avg_rating', 'checkouts'), reverse=True)
    limit = request.GET.get('limit', 25)
    context = {'books': sorted_b[:limit]}
    return render_to_response('circulation/top.html', context)


#########################################################
## Reports
def others_read_report(request, **kwargs):
    book_id = None
    errors = False
    patron = None
    try:
        patron = get_object_or_404(Patron, pk=kwargs['patron_id'])
        if request.GET['book_id'] != "":
            book_id = request.GET['book_id']
        else:
            errors = "Must select a book"
    except MultiValueDictKeyError:
        pass
    if book_id is not None:
        book_counts = {}
        book_checkouts = Checkout.objects.filter(book__id=book_id)
        for book_checkout in book_checkouts:
            if book_checkout.patron.id == patron.id:
                continue
            for patron_checkout in Checkout.objects.filter(patron__id=book_checkout.patron.id):
                if patron_checkout.book.id == book_id:
                    continue
                try:
                    book_counts[patron_checkout.book]['count'] += 1
                except:
                    book_counts[patron_checkout.book] = {'book': patron_checkout.book, 'count': 1}
        sorted_books = [bc[1]['book'] for bc in (sorted(book_counts.items(), key=lambda book_count_entry: book_count_entry[1]['count']))]
        context = {'item_list': sorted_books, 'is_paginated': False}
        return render_to_response('books/list.html', context)
    else:
        checkout_history = Checkout.objects.filter(patron=patron).order_by('book__title')
        books = [x.book for x in checkout_history]
        return render_to_response('reports/book_selection.html', {'patron': patron, 'books': books, 'errors': errors})

def reports_patron_index(request, **kwargs):
    patron = get_object_or_404(Patron, pk=kwargs['patron_id'])
    context = {'patron': patron}
    return render_to_response('reports/report_selection.html', context)

def reports_home_select_patron(request):
    return render_to_response('reports/home.html', {'patrons': Patron.objects.all().order_by('last_name', 'first_name')})
        