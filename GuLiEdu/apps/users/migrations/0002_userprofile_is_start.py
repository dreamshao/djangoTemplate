# Generated by Django 3.2.25 on 2025-03-13 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_start',
            field=models.BooleanField(default=False, verbose_name='是否激活'),
        ),
    ]
