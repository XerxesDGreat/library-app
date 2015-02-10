# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20150202_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='checkin_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='checkout',
            name='checkout_date',
            field=models.DateField(),
            preserve_default=True,
        ),
    ]
