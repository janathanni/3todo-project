# Generated by Django 4.0.1 on 2022-12-10 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_user_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]