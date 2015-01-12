from django.conf.urls import patterns, url

from library import views

urlpatterns = patterns('',
    url(r'^book/?', views.BookIndexView.as_view(), name='index'),
)