# Generated by Django 5.0.3 on 2024-06-06 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0019_location_radius'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='radius',
            field=models.FloatField(blank=True, null=True),
        ),
    ]