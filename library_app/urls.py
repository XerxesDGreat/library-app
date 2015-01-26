from django.conf.urls import patterns, include, url
from django.contrib import admin

from library import views

urlpatterns = patterns('',
    url(r'', include('library.urls', namespace='library')),
    url(r'^admin/', include(admin.site.urls))
)
