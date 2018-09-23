# Generated by Django 2.0.6 on 2018-09-17 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbmodels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='')),
                ('img_type', models.IntegerField(choices=[(0, '轮播'), (1, '最热'), (2, '最新')])),
                ('stat', models.IntegerField(choices=[(0, '下架'), (1, '上架')])),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='header_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]