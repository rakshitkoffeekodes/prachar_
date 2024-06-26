# Generated by Django 5.0.6 on 2024-06-25 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0057_alter_assigndevice_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True, verbose_name='Created At')),
                ('area_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('radius', models.IntegerField(verbose_name='Radius')),
                ('created_by', models.ForeignKey(db_column='created_by', on_delete=django.db.models.deletion.PROTECT, to='p_app.userdetails', verbose_name='Created By')),
            ],
            options={
                'verbose_name_plural': 'Area',
            },
        ),
    ]
