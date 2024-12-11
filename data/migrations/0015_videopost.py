# Generated by Django 4.2.16 on 2024-12-04 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_donationrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('video', models.FileField(upload_to='videos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
