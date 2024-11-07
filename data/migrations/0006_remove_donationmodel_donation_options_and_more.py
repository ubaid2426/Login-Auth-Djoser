# Generated by Django 4.2.16 on 2024-11-06 06:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_donationoption_donationmodel_donation_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donationmodel',
            name='donation_options',
        ),
        migrations.CreateModel(
            name='DonationHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='data.donationmodel')),
            ],
        ),
    ]
