# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='copyright',
            new_name='published',
        ),
        migrations.RemoveField(
            model_name='author',
            name='birthday',
        ),
    ]
