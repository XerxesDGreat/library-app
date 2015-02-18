__author__ = 'josh'

from django.forms import widgets
from django.utils.safestring import mark_safe
from library.models import Author
import re

class TypeAheadWidget(widgets.Widget):
    '''
    This provides the backend for a set of input elements used for auto-completion of search terms.

    The visible element is called "{name}_autocomplete" and this will hold the string. The hidden element, "{name}_autocomplete_id",
    will actually contain the real value of the field. The corresponding javascript will make the visible element into a
    JQueryUI-powered autocomplete box and will populate the hidden element when a value is selected. If no value is
    selected from the autocomplete choices (provided by a search), then the typed-in string will be used to select or
    add a new record, if possible.
    '''

    def __init__(self, model, attrs=None):#addl_query_args=None, attrs=None):
        super(TypeAheadWidget, self).__init__(attrs)
        self.model = model
        #self.browse_url = browse_url,
        #self.return_url = return_url
        #self.addl_query_args = {} if addl_query_args is None else addl_query_args

    def render(self, name, value, attrs=None):
        '''
        Renders the form fields
        :var name: str
        :var value: str
        :var attrs: dict
        :return:
        '''
        try:
            item = self.model.objects.get(pk=value)
        except:
            item = None
        str_template = '<input type="text" name="{name}_text" id="{name}_autocomplete" value="{friendly_name}" />' \
            + '<input type="hidden" name="{name}" value="{item_id}" id="{name}_autocomplete_id" />'
        repl = {
            'name': name,
            'friendly_name': item.form_display_text() if item else '',
            'item_id': item.id if item else ''
        }
        return mark_safe(str_template.format(**repl))

    def value_from_datadict(self, data, files, name):
        '''
        Creates the python value from the given datadict, containing all the fields in the form
        :param data:
        :param files:
        :param name:
        :return:
        '''
        autocompleted = data.get(name)
        provided = data.get('%s_text' % name)
        if autocompleted:
            try:
                value = self.model.objects.get(pk=autocompleted)
            except:
                value = None
        elif provided:
            value = self.model.build_from_value(provided)
        else:
            value = None
        return None if value is None else value.id