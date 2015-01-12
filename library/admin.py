from django.contrib import admin
from library.models import Author, Student, Book, Checkout, Rating

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Checkout)
admin.site.register(Rating)
admin.site.register(Student)
