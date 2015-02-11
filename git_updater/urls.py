__author__ = 'josh'
from django.conf.urls import patterns, url

from git_updater import views

urlpatterns = patterns('',
    # author urls
    url(r'^admin/updates/$', views.UpdatesListView.as_view(), name='update_list'),
    url(r'^admin/updates/apply/$', views.apply_all_updates, name='do_updates')
)