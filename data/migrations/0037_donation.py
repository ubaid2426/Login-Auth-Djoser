# Generated by Django 4.2.16 on 2025-01-04 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0036_bloodrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('contact_number', models.CharField(max_length=15)),
                ('current_location', models.CharField(max_length=255)),
                ('donation_type', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
            ],
        ),
    ]
