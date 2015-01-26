from django.conf.urls import patterns, url

from library import views
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # author urls
    url(r'^authors/create/', views.AuthorCreateView.as_view(), name='author_add'),
    url(r'^authors/$', views.AuthorIndexView.as_view(), name='author_index'),
    # book urls
    url(r'^books/(?P<pk>\d+)/update/$', views.BookUpdateView.as_view(), name='book_update'),
    url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^books/create/$', views.BookCreateView.as_view(), name='book_create'),
    url(r'^books/$', views.BookIndexView.as_view(), name='book_index'),
    # student urls
    url(r'^students/(?P<pk>\d+)/$', views.StudentDetailView.as_view(), name='student_detail'),
    url(r'^students/(?P<pk>\d+)/update/$', views.StudentUpdateView.as_view(), name='student_update'),
    url(r'^students/create/$', views.StudentCreateView.as_view(), name='student_create'),
    url(r'^students/$', views.StudentIndexView.as_view(), name='student_index'),
    # circulation urls
    url(r'^circulation/(?P<pk>\d+)/$', views.CirculationDetailView.as_view(), name='circulation_detail'),
    url(r'^circulation/create/$', views.CirculationCreateView.as_view(), name='circulation_create'),
    url(r'^circulation/student/(?P<pk>\d+)/$', views.CirculationIndexByStudentView.as_view(), name='circulation_student_index'),
    url(r'^circulation/all/$', views.CirculationIndexView.as_view(), name='circulation_index'),
    url(r'^circulation/$', TemplateView.as_view(template_name='circulation/home.html'), name='circulation_home'),
    # report urls
    url(r'^reports/(?P<student_id>\d+)/others_read/$', views.others_read_report, name='reports_others_read'),
    url(r'^reports/(?P<student_id>\d+)/$', views.reports_student_index, name='reports_student_index'),
    url(r'^reports/$', views.reports_home_select_student, name='reports_home'),
)