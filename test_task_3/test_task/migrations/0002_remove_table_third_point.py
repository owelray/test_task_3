# Generated by Django 3.1 on 2021-01-23 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_task', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='third_point',
        ),
    ]