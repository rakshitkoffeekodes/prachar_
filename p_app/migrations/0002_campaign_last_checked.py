# Generated by Django 5.0.6 on 2024-06-22 13:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='last_checked',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Last Checked'),
        ),
    ]
