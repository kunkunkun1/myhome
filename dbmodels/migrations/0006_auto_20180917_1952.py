# Generated by Django 2.0.6 on 2018-09-17 11:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dbmodels', '0005_auto_20180917_1940'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='showimg',
            options={'verbose_name': '首页展示图片', 'verbose_name_plural': '首页展示图片'},
        ),
        migrations.AddField(
            model_name='showimg',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='showimg',
            name='top',
            field=models.BooleanField(default=False),
        ),
    ]
