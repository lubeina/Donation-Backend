# Generated by Django 2.2.7 on 2020-03-31 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20200331_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='points',
        ),
    ]