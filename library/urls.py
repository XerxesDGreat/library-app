from django.conf.urls import patterns, url

from library import views
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    # author urls
    url(r'^authors/create/', views.AuthorCreateView.as_view(), name='author_add'),
    url(r'^authors/search/$', views.author_search, name='author_search'),
    url(r'^authors/$', views.AuthorIndexView.as_view(), name='author_index'),
    # book urls
    url(r'^books/(?P<pk>\d+)/update/$', views.BookUpdateView.as_view(), name='book_update'),
    url(r'^books/(?P<pk>\d+)/$', views.BookDetailView.as_view(), name='book_detail'),
    url(r'^books/create/$', views.BookCreateView.as_view(), name='book_create'),
    url(r'^books/search/title/$', views.book_title_search, name='book_search'),
    url(r'^books/$', views.BookIndexView.as_view(), name='book_index'),
    # patron urls
    url(r'^patrons/(?P<pk>\d+)/$', views.PatronDetailView.as_view(), name='patron_detail'),
    url(r'^patrons/(?P<pk>\d+)/update/$', views.PatronUpdateView.as_view(), name='patron_update'),
    url(r'^patrons/create/$', views.PatronCreateView.as_view(), name='patron_create'),
    url(r'^patrons/search/$', views.patron_search, name='patron_search'),
    url(r'^patrons/$', views.PatronIndexView.as_view(), name='patron_index'),
    # circulation urls
    url(r'^circulation/top/$', views.highest_rated_titles, name='circulation_top'),
    url(r'^circulation/(?P<pk>\d+)/$', views.CirculationDetailView.as_view(), name='circulation_detail'),
    url(r'^circulation/create/$', views.CirculationCreateView.as_view(), name='circulation_create'),
    url(r'^circulation/patron/(?P<pk>\d+)/$', views.CirculationIndexByPatronView.as_view(), name='circulation_patron_index'),
    url(r'^circulation/all/$', views.CirculationIndexView.as_view(), name='circulation_index'),
    url(r'^circulation/$', TemplateView.as_view(template_name='circulation/home.html'), name='circulation_home'),
    # report urls
    url(r'^reports/(?P<patron_id>\d+)/others_read/$', views.others_read_report, name='reports_others_read'),
    url(r'^reports/(?P<patron_id>\d+)/$', views.reports_patron_index, name='reports_patron_index'),
    url(r'^reports/$', views.reports_home_select_patron, name='reports_home'),
)