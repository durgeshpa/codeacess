# Generated by Django 3.1.7 on 2021-04-08 20:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='mobile',
            field=models.CharField(blank=True, max_length=13, null=True, validators=[django.core.validators.RegexValidator('^[\\+0-9]$')]),
        ),
    ]