# Generated by Django 2.2.3 on 2019-07-11 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20190711_1607'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='tiemstamp',
            new_name='timestamp',
        ),
    ]
