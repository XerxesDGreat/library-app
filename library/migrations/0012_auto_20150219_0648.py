# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection, migrations
import sqlite3

def modify_db_dates(apps, schema_editor):
    '''
    Migrates the data from datetime to just plain date; this is the data migration for the schema change in migration 11

    This needs to use actual raw sql due to the fact that, by the time the data gets to the models, the fact that the
    values are datetime in the db ends up making the value in models None because datetime doesn't deserialize to date.
    And by "actual raw sql", I apparently can't even use the django db engine; it corrupts the data even there.
    '''
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute('SELECT id, checkout_date, checkin_date FROM library_checkout;')
    new_values = []
    def get_date(date_time):
        if date_time is None or ' ' not in date_time:
            return date_time
        return date_time.split(' ')[0]
    for row in c.fetchall():
        new_values.append((get_date(row[1]), get_date(row[2]), row[0]))

    c.executemany('UPDATE library_checkout SET checkout_date=?, checkin_date=? WHERE id=?', new_values)
    conn.commit()

class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20150210_0757'),
    ]

    operations = [
        migrations.RunPython(modify_db_dates)
    ]
