# Generated by Django 5.0.3 on 2024-06-10 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0033_alter_campaign_cm_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='cm_end_date',
            field=models.DateField(editable=False, verbose_name='End Date'),
        ),
        migrations.AlterField(
            model_name='captain',
            name='c_contact_no',
            field=models.CharField(max_length=10, verbose_name='Contact Number'),
        ),
    ]
