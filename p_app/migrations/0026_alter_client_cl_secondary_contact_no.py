# Generated by Django 5.0.3 on 2024-06-07 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0025_alter_client_cl_secondary_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cl_secondary_contact_no',
            field=models.IntegerField(blank=True, null=True, verbose_name='Secondary Contact Number'),
        ),
    ]