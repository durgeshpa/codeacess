# Generated by Django 3.1.7 on 2021-04-13 22:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programing', '0021_auto_20210413_2158'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='CLanguage',
            new_name='title',
        ),
    ]
