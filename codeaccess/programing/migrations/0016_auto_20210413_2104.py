# Generated by Django 3.1.7 on 2021-04-13 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programing', '0015_auto_20210413_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='title',
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.ForeignKey(default=1, on_delete=set, to='programing.clanguage'),
            preserve_default=False,
        ),
    ]
