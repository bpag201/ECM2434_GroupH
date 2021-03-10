# Generated by Django 3.1.6 on 2021-02-10 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('study_platform', '0002_auto_20210210_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_platform.userprofile'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='participants',
            field=models.ManyToManyField(to='study_platform.UserProfile'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='study_platform.userprofile'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='study_platform.userprofile'),
        ),
        migrations.AlterField(
            model_name='reward',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_platform.userprofile'),
        ),
        migrations.AlterField(
            model_name='team',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='study_platform.userprofile'),
        ),
        migrations.AlterField(
            model_name='teamblog',
            name='participants',
            field=models.ManyToManyField(to='study_platform.UserProfile'),
        ),
        migrations.AlterField(
            model_name='usertitle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_platform.userprofile'),
        ),
        migrations.AlterField(
            model_name='welfareresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='study_platform.userprofile'),
        ),
    ]