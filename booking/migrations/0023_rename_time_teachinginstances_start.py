# Generated by Django 3.2.8 on 2022-02-27 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0022_performancedetails_concert_dress'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachinginstances',
            old_name='time',
            new_name='start',
        ),
    ]
