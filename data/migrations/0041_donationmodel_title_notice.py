# Generated by Django 4.2.16 on 2025-01-08 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0040_donationrequest_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='donationmodel',
            name='title_notice',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
