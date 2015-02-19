# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from library.models import Author

import re

def populate_last_name_from_comma_separated_first_name(apps, schema_editor):
    authors = Author.objects.filter(last_name__isnull=True)
    for author in authors:
        '''
        There are a few different cases possible where there is only a first name:
        1) "LastName, FirstName," (most common)
        2) "LastName, FirstName MiddleInit." (note no comma at the end; seems to only happen with middle initial
        3) "OnlyName" (from the examples I saw, probably only last name and first name vanished, or something like "Madonna")
        4) "Corporation Name" (i.e. "Walt Disney Company"; should be in publisher)
        5) "Series Name" (rare; could be just the one instance)
        6) Just some plain weird crap that I hope I can figure out programmatically; lexically the same as 4) or 5)

        Since there are different assumptions, we'll be having a bunch of fun :-/
        '''
        if ',' in author.first_name:
            n = author.first_name.rstrip(' ,.')
            parts = n.split(', ')
            if len(parts) > 2:
                date_match = re.compile(r'[0-9]{4}-[0-9]{4}')
                if parts[-1] == 'ill' or date_match.match(parts[-1]):
                    parts.pop(-1)
                elif parts[-1] == 'and Electric':
                    continue
                elif ' and ' in parts[1]:
                    a1f, a2l = parts[1].split(' and ')
                    a1l = parts[0]
                    a2f = parts[2]
                    new_author = Author(first_name=a2f, last_name=a2l)
                    new_author.save()
                    author.first_name = a1f
                    author.last_name = a1l
                    author.save()
                    print ('split out %s from %s' % (new_author.full_name(), author.full_name()))
                    continue
            # now, parts are 2 pieces
            author.first_name = parts[1]
            author.last_name = parts[0]
            author.save()
        elif ';' in author.first_name:
            n = author.first_name.rstrip(' ,.')
            parts = n.split('; ')
            for i in range(0, len(parts)):
                if parts[i] == 'et al' or 'Media' in parts[i] or 'Productions' in parts[i]:
                    continue
                nameparts = parts[i].split(' ')
                if len(nameparts) > 2:
                    f = nameparts[0] + ' ' + nameparts[1]
                else:
                    f = nameparts[0]
                l = nameparts[-1]
                a = Author() if i else author
                a.first_name = f
                a.last_name = l
                a.save()
            print ('broke up %s into different names' % n)
        elif author.first_name == 'C. Levin and M.':
            author.first_name = 'C.'
            author.last_name = 'Levin'
            author.save()
        else:
            author.first_name.strip(' ')
            check_name(author, 'Milne A. A.', 'A. A.', 'Milne')
            check_name(author, 'Stine R L', 'R. L.', 'Stine')
            check_name(author, 'De la Bedoyere Camilla', 'Camilla', 'de la Bedoyere')
            check_name(author, 'Bablyoan R.', 'R.', 'Babloyan')
            check_name(author, 'Louisa May Alcott.', 'Louisa May', 'Alcott')
            check_name(author, 'Dorling Kindersley', 'Dorling', 'Kindersley')
            check_name(author, 'Yehuda Shiff', 'Yehuda', 'Shiff')
            check_name(author, 'Milne A. A.', 'A. A.', 'Milne')
            check_name(author, 'Shula Modan', 'Shula', 'Modan')
            check_name(author, 'Susan V.', 'Susan', 'V.')
            check_name(author, 'Phyllis Reynolds Naylor', 'Phyllis Reynolds', 'Naylor')
            check_name(author, 'Sharon Robinson', 'Sharon', 'Robinson')
            check_name(author, 'Harriet K.', 'Harriet', 'K.')
            check_name(author, 'Lea Levavi', 'Lea', 'Levavi')
            check_name(author, 'Shlomo Ariel', 'Shlomo', 'Ariel')
            check_name(author, 'Atara Ofek', 'Atara', 'Ofek')
            check_name(author, 'Fabio Bourbon', 'Fabio', 'Bourbon')
            check_name(author, 'Cicely Mary Barker', 'Cicely Mary', 'Barker')
            check_name(author, 'Suzy Kline', 'Suzy', 'Kline')
            check_name(author, 'Noam Sachs Zion', 'Noam Sachs', 'Zion')
            check_name(author, 'Liu Jae Soo', 'Liu Jae', 'Soo')
            author.save()


def check_name(author, full_name, first_name, last_name):
    if author.first_name == full_name:
        author.first_name = first_name
        author.last_name = last_name
        print 'changed %s to [%s][%s]' % (full_name, first_name, last_name)



class Migration(migrations.Migration):

    dependencies = [
        ('library', '0013_auto_20150219_0734'),
    ]

    operations = [
        migrations.RunPython(populate_last_name_from_comma_separated_first_name)
    ]
