# Generated by Django 5.0.3 on 2024-06-13 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0046_remove_assigndevice_ad_captain_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigndevice',
            name='ad_assign_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Assign', 'Assign')], max_length=50, null=True),
        ),
    ]