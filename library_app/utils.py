'''
Created on Jan 13, 2015

@author: josh
'''
from django.core.urlresolvers import reverse as django_reverse

def reverse(viewname, urlconf = None, args = None, kwargs = None, prefix = None, current_app = None, query_args = None):
    """
    Wrapper of django.core.urlresolvers.reverse that attaches arguments in kwargs as query string parameters
    """
    url = django_reverse(viewname, urlconf, args, kwargs, prefix, current_app)
    if query_args:
        url = '%s?%s' % (url, '&'.join(['%s=%s' % (k,v) for k,v in query_args.items()]))
    return url 