# Generated by Django 3.2.8 on 2022-05-31 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0027_auto_20220314_2003'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_number',
            field=models.CharField(default='please change', editable=False, max_length=32),
            preserve_default=False,
        ),
    ]
