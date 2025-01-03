# Generated by Django 4.2.16 on 2025-01-01 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0035_donationmodel_address_donationmodel_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BloodRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15)),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('distance_km', models.FloatField()),
                ('time_required', models.DurationField(help_text='Time in HH:MM:SS format')),
                ('quantity', models.PositiveIntegerField(help_text='Quantity in liters')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
