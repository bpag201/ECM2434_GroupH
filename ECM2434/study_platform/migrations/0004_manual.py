# Generated by Django 3.1.6 on 2021-02-10 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_platform', '0003_auto_20210210_1401'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
