# Generated by Django 3.2.8 on 2022-01-29 14:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0016_auto_20220129_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teachingdetails',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='booking.booking'),
        ),
    ]
