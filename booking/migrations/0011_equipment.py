# Generated by Django 3.2.8 on 2021-12-11 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_auto_20211209_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(choices=[('WORLD', 'World'), ('POP', 'Pop'), ('CONTEMPORARY', 'Contemporary'), ('ORCHESTRAL', 'Orchestral'), ('OTHER', 'Other')], max_length=32)),
                ('daily_hire_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('description', models.CharField(max_length=254)),
                ('equipment_type', models.CharField(max_length=32)),
            ],
        ),
    ]
