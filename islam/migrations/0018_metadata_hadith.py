# Generated by Django 4.2.16 on 2024-12-08 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0017_delete_hadith_delete_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.CharField(max_length=2555, null=True)),
                ('arabic_title', models.CharField(max_length=2555)),
                ('arabic_author', models.CharField(max_length=2555)),
                ('arabic_introduction', models.TextField()),
                ('english_title', models.CharField(max_length=2555)),
                ('english_author', models.CharField(max_length=2555)),
                ('english_introduction', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Hadith',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hadith_id', models.IntegerField()),
                ('id_in_book', models.IntegerField()),
                ('chapter_id', models.IntegerField()),
                ('book_id', models.IntegerField()),
                ('arabic_hadith', models.TextField()),
                ('english_narrator', models.CharField(max_length=2555)),
                ('english_text', models.TextField()),
                ('metadata', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hadiths', to='islam.metadata')),
            ],
        ),
    ]