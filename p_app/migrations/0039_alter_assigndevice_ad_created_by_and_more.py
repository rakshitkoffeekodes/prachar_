# Generated by Django 5.0.3 on 2024-06-11 10:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0038_alter_client_created_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='assigndevice',
            name='ad_created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='country',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='state',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AlterField(
            model_name='vehiclelicenseinformation',
            name='created_by',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
    ]
