# Generated by Django 4.2.16 on 2024-11-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0006_surah1_juz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surah1',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]