# Generated by Django 5.0.3 on 2024-06-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0018_locationuuid_withquotas_alter_location_lat_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='radius',
            field=models.JSONField(null=True),
        ),
    ]
