from django.views import generic

from library.models import Author, Book, Student, Checkout
from library_app.utils import reverse
from library.forms import BookForm, CheckoutForm#, AuthorForm, StudentForm
    
#########################################################
## Authors
class AuthorIndexView(generic.ListView):
    template_name='authors/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        try:
            context['added_id'] = self.request.GET['added_id']
        except:
            pass
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

#########################################################
## Books
class BookIndexView(generic.ListView):
    template_name = 'books/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        try:
            context['added_id'] = self.request.GET['added_id']
        except:
            pass
        return context
    
    def get_queryset(self):
        return Book.objects.order_by('title')

class BookDetailView(generic.UpdateView):
    form_class = BookForm
    model = Book
    fields = ['title', 'author', 'published']
    template_name = 'books/form.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        context['form_action'] = 'add' if self.object is None else 'edit'
        return context
    
    def get_success_url(self):
        query_args = None
        if self.object:
            query_args = {'edited': self.object.id}
            
        return reverse('library:book_index', query_args=query_args)

class BookCreateView(generic.CreateView):
    model = Book
    fields = ['title', 'author']
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['book'] = self.object
        return context_data
    
    def get_success_url(self):
        return reverse('library:book_list', query_args={'added_id': self.object.id})
    
#########################################################
## Students
class StudentIndexView(generic.ListView):
    template_name = 'students/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        try:
            context['added_id'] = self.request.GET['added_id']
        except:
            pass
        return context
    
    def get_queryset(self):
        return Student.objects.order_by('last_name', 'first_name')

class StudentDetailView(generic.UpdateView):
    #form_class = StudentForm
    model = Student
    fields = ['first_name', 'last_name', 'grade']
    template_name = 'students/form.html'
    
    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        context['form_action'] = 'add' if self.object is None else 'edit'
        return context
    
    def get_success_url(self):
        query_args = None
        if self.object:
            query_args = {'edited': self.object.id}
            
        return reverse('library:student_index', query_args=query_args)

class StudentCreateView(generic.CreateView):
    model = Student
    fields = ['first_name', 'last_name', 'grade']
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['student'] = self.object
        return context_data
    
    def get_success_url(self):
        return reverse('library:student_index', query_args={'added_id': self.object.id})
    
#########################################################
## Circulation
class CirculationIndexView(generic.ListView):
    template_name = 'circulation/list.html'
    context_object_name = 'item_list'
    paginate_by = 25
    
    def get_queryset(self):
        return Checkout.objects.order_by('-checkout_date', '-checkin_date', 'book__title')

class CirculationDetailView(generic.UpdateView):
    form_class = CheckoutForm
    model = Checkout
    fields = ['checkout_date', 'checkin_date', 'student', 'book']
    template_name = 'circulation/form.html'
    
    def get_context_data(self, **kwargs):
        context = super(CirculationDetailView, self).get_context_data(**kwargs)
        context['form_action'] = 'add' if self.object is None else 'edit'
        return context
    
    def get_success_url(self):
        query_args = None
        if self.object:
            query_args = {'edited': self.object.id}
            
        return reverse('library:circulation_index', query_args=query_args)
    
class CirculationCreateView(generic.CreateView):
    model = Checkout
    form_class = CheckoutForm
    #fields = ['checkout_date', 'checkin_date', 'book', 'student']
    
    def get_context_data(self, **kwargs):
        context_data = generic.CreateView.get_context_data(self, **kwargs)
        context_data['checkout'] = self.object
        return context_data
    
    def get_success_url(self):
        return reverse('library:circulation_list', query_args={'added_id': self.object.id})