# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_report_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('id',)},
        ),
    ]
