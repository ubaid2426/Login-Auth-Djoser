# Generated by Django 4.2.16 on 2024-11-16 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surah',
            old_name='name',
            new_name='nameAr',
        ),
        migrations.RenameField(
            model_name='surah',
            old_name='transliteration',
            new_name='nameEn',
        ),
        migrations.RenameField(
            model_name='surah',
            old_name='total_verses',
            new_name='total_ayat',
        ),
    ]