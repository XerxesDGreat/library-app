'''
Created on Jan 27, 2015

@author: josh
'''
from django import template
from git_updater.utils import get_available_updates
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def iter_range( value ):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range( value )

class NoUpdatesNode(template.Node):
    def render(self, context):
        return "Everything is up to date"

class UpdatesNode(template.Node):
    def __init__(self, num_updates, url_target):
        self.num_updates = num_updates
        self.url_target = url_target

    def render(self, context):
        update_str = "There is 1 available update" if self.num_updates == 1 else "There are %d available updates" % self.num_updates
        print self.url_target
        url = reverse(self.url_target)
        return '%s. <a href="%s">Click here</a> to update!' % (update_str, url)

@register.tag("check_for_updates")
def do_check_for_updates(parser, token):
    available_updates = get_available_updates()
    try:
        tag_name, url_target = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '%r tag requires a single argument' % token.contents.split()[0]
        )
    if len(available_updates):
        return UpdatesNode(num_updates=len(available_updates), url_target=url_target)
    else:
        return NoUpdatesNode()