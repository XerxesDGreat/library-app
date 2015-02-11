__author__ = 'josh'
from git_updater import utils
from django.views.generic import ListView
from django.http.response import StreamingHttpResponse

class UpdatesListView(ListView):
    template_name = 'updates/list.html'

    def get_context_data(self, **kwargs):
        context = super(UpdatesListView, self).get_context_data(**kwargs)
        context['version'] = utils.get_current_version()
        return context

    def get_queryset(self):
        return utils.get_available_updates()

def apply_all_updates(request, **kwargs):
    return StreamingHttpResponse(utils.do_update())