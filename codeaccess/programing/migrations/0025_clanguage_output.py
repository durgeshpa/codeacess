# Generated by Django 3.1.7 on 2021-04-19 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programing', '0024_clanguage_lavel'),
    ]

    operations = [
        migrations.AddField(
            model_name='clanguage',
            name='output',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
