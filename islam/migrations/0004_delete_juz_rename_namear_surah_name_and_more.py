# Generated by Django 4.2.16 on 2024-11-23 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0003_juz'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Juz',
        ),
        migrations.RenameField(
            model_name='surah',
            old_name='nameAr',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='surah',
            old_name='total_ayat',
            new_name='total_verses',
        ),
        migrations.RenameField(
            model_name='surah',
            old_name='nameEn',
            new_name='transliteration',
        ),
    ]
