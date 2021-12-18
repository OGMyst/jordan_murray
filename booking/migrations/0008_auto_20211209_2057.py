# Generated by Django 3.2.8 on 2021-12-09 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_address'),
        ('booking', '0007_auto_20211208_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_type',
            field=models.CharField(choices=[('TEACHING', 'Teaching'), ('PERFORMANCE', 'Performance'), ('EQUIPMENT', 'Equipment hire'), ('TEACHING AND EQUIPMENT', 'Teaching and Equipment hire')], max_length=32),
        ),
        migrations.CreateModel(
            name='PerformanceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('performance_type', models.CharField(choices=[('REHEARSAL', 'Rehearsal'), ('PERFORMANCE', 'Performance')], max_length=32)),
                ('session_cost', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10)),
                ('description', models.CharField(blank=True, max_length=254)),
                ('Address', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.address')),
                ('booking_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.booking')),
            ],
        ),
    ]