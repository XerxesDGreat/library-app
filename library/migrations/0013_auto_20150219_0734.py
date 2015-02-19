# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sqlite3

def clean_up_first_names(apps, schema_editor):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, first_name FROM library_author;')
    for row in c.fetchall():
        if '.' not in row[1]:
            continue
        o = row[1]
        parts = o.split('.')
        if len(parts) < 2:
            continue
        if parts[1] == '':
            name_parts = parts[0].split(' ')
            name_parts = [('%s.' % x if len(x) == 1 else x).strip() for x in name_parts]
            fname = ' '.join(name_parts)
        else:
            fname = '. '.join([x.strip() for x in parts[:-1]]) + '.'
        c.execute('UPDATE library_author SET first_name="%s" where id=%s;' % (fname, row[0]))
    conn.commit()



class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_auto_20150219_0648'),
    ]

    operations = [
        migrations.RunPython(clean_up_first_names)
    ]
