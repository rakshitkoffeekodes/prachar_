# Generated by Django 5.0.6 on 2024-06-22 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0003_remove_campaign_last_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='last_retrieval',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Last Retrieval Time'),
        ),
    ]