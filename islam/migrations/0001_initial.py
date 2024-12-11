# Generated by Django 4.2.16 on 2024-11-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Surah',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('transliteration', models.CharField(max_length=255)),
                ('translation', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=50)),
                ('total_verses', models.IntegerField()),
            ],
        ),
    ]
