# Generated by Django 2.0.6 on 2018-09-18 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmodels', '0009_auto_20180918_0835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rightnav',
            options={'verbose_name': '右侧导航', 'verbose_name_plural': '右侧导航'},
        ),
        migrations.AddField(
            model_name='rightnav',
            name='icon',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
