# Generated by Django 5.0.3 on 2024-06-13 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0047_assigndevice_ad_assign_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assigndevice',
            name='ad_assign_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Assign', 'Assign')], default='Pending', max_length=50, null=True),
        ),
    ]
