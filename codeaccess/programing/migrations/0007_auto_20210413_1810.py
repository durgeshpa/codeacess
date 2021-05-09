# Generated by Django 3.1.7 on 2021-04-13 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programing', '0006_auto_20210413_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clanguage',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='c_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]