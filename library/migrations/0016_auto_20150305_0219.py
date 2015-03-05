# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_auto_20150305_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True, choices=[(None, b'-- no rating --'), (5, b'Loved it'), (4, b'Liked it'), (3, b'Meh'), (2, b'Not good'), (1, b'Hated it')]),
            preserve_default=True,
        ),
    ]
