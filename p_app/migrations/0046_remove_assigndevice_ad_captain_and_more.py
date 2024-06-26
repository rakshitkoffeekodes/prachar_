# Generated by Django 5.0.3 on 2024-06-13 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0045_alter_campaign_cm_geo_fencing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assigndevice',
            name='ad_captain',
        ),
        migrations.RemoveField(
            model_name='vehiclelicenseinformation',
            name='vi_captain',
        ),
        migrations.AddField(
            model_name='captain',
            name='c_assign_device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='p_app.assigndevice', verbose_name='Assign Device'),
        ),
        migrations.AddField(
            model_name='captain',
            name='c_vehicle_license_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='p_app.vehiclelicenseinformation', verbose_name='Vehicle License'),
        ),
        migrations.AlterField(
            model_name='captain',
            name='c_contact_no',
            field=models.IntegerField(verbose_name='Contact Number'),
        ),
    ]
