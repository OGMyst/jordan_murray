# Generated by Django 3.2.8 on 2021-12-11 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0011_equipment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmenthiredetails',
            name='pick_up_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='equipmenthiredetails',
            name='return_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='performancedetails',
            name='session_cost',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='teachingdetails',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
