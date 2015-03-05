from django.contrib import admin
from library.models import Author, Patron, Book, Checkout

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Checkout)
admin.site.register(Patron)
