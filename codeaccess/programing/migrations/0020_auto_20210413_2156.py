# Generated by Django 3.1.7 on 2021-04-13 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programing', '0019_auto_20210413_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clanguage',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.ManyToManyField(blank=True, to='programing.CLanguage'),
        ),
    ]
