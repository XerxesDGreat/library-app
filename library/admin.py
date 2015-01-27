from django.contrib import admin
from library.models import Author, Patron, Book, Checkout, Rating

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Checkout)
admin.site.register(Rating)
admin.site.register(Patron)
