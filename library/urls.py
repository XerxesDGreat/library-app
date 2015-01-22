from django.conf.urls import patterns, url

from library import views

urlpatterns = patterns('',
    # author urls
    url(r'^authors/create/', views.AuthorCreateView.as_view(), name='author_add'),
    url(r'^authors/$', views.AuthorIndexView.as_view(), name='author_index'),
    # book urls
    url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^books/create/$', views.BookCreateView.as_view(), name='book_create'),
    url(r'^books/$', views.BookIndexView.as_view(), name='book_index'),
    # student urls
    url(r'^students/(?P<pk>\d+)/$', views.StudentDetailView.as_view(), name='student_detail'),
    url(r'^students/create/$', views.StudentCreateView.as_view(), name='student_create'),
    url(r'^students/$', views.StudentIndexView.as_view(), name='student_index'),
    # circulation urls
    url(r'^circulation/(?P<pk>\d+)/$', views.CirculationDetailView.as_view(), name='circulation_detail'),
    url(r'^circulation/create/$', views.CirculationCreateView.as_view(), name='circulation_create'),
    url(r'^circulation/$', views.CirculationIndexView.as_view(), name='circulation_index'),
)