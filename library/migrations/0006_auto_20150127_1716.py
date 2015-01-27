# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_auto_20150126_1903'),
    ]

    operations = [
        migrations.RenameModel('Student','Patron'),
        migrations.AlterField(
            model_name='checkout',
            name='student',
            field=models.ForeignKey(to='library.Patron'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rating',
            name='student',
            field=models.ForeignKey(to='library.Patron'),
            preserve_default=True,
        ),
        migrations.RenameField('Checkout', 'student', 'patron'),
        migrations.RenameField('Rating', 'student', 'patron'),
    ]
