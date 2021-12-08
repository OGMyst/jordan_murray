# Generated by Django 3.2.8 on 2021-12-06 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('booking', '0003_alter_enquiry_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='userprofile',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.userprofile'),
        ),
    ]
