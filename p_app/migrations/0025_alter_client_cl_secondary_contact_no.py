# Generated by Django 5.0.3 on 2024-06-07 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0024_alter_city_created_by_alter_client_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cl_secondary_contact_no',
            field=models.IntegerField(blank=True, verbose_name='Secondary Contact Number'),
        ),
    ]
