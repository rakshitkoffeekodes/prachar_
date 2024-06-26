# Generated by Django 5.0.3 on 2024-06-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_app', '0032_alter_campaign_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='cm_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Running', 'Running'), ('Completed', 'Completed')], editable=False, max_length=50, verbose_name='Status'),
        ),
    ]
