# Generated by Django 5.0.3 on 2024-06-06 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0016_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='lon',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
