# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='race_choice',
            field=models.CharField(default=b'HUM', max_length=3, choices=[(b'HUM', b'Human'), (b'ELF', b'Elf')]),
        ),
    ]
