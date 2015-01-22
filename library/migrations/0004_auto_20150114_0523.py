# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_student_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='comments',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
