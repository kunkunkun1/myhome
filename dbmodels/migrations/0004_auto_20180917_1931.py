# Generated by Django 2.0.6 on 2018-09-17 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmodels', '0003_auto_20180917_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='login_account',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
