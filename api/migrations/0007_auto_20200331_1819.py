# Generated by Django 2.2.7 on 2020-03-31 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200331_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]