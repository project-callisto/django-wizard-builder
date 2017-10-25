# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 00:15
from __future__ import unicode_literals

import wizard_builder.model_helpers

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wizard_builder', '0035_auto_20171025_0014'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleChoice',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('wizard_builder.formquestion',),
        ),
        migrations.CreateModel(
            name='SingleLineText',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=(wizard_builder.model_helpers.ProxyQuestion, 'wizard_builder.formquestion'),
        ),
        migrations.CreateModel(
            name='TextArea',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=(wizard_builder.model_helpers.ProxyQuestion, 'wizard_builder.formquestion'),
        ),
        migrations.CreateModel(
            name='Checkbox',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=(wizard_builder.model_helpers.ProxyQuestion, 'wizard_builder.multiplechoice'),
        ),
        migrations.CreateModel(
            name='RadioButton',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=(wizard_builder.model_helpers.ProxyQuestion, 'wizard_builder.multiplechoice'),
        ),
    ]