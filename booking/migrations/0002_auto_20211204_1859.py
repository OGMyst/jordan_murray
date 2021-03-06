# Generated by Django 3.2.8 on 2021-12-04 18:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enquiry',
            old_name='dates',
            new_name='booking_details',
        ),
        migrations.RenameField(
            model_name='enquiry',
            old_name='email',
            new_name='contact_email',
        ),
        migrations.RenameField(
            model_name='enquiry',
            old_name='full_name',
            new_name='contact_name',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='description',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='equipment',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='location',
        ),
        migrations.RemoveField(
            model_name='enquiry',
            name='times',
        ),
        migrations.AddField(
            model_name='enquiry',
            name='date_submitted',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
