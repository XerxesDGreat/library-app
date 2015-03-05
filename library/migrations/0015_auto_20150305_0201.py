# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_auto_20150226_0738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='book',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='patron',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.AddField(
            model_name='checkout',
            name='rating',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
