# Generated by Django 3.2.8 on 2022-01-29 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0018_auto_20220129_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachingdetails',
            name='payment_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
