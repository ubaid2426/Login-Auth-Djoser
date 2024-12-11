# Generated by Django 4.2.16 on 2024-11-27 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('islam', '0007_alter_surah1_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surah1',
            name='verse',
        ),
        migrations.AlterField(
            model_name='juz',
            name='end_verse',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='juz',
            name='index',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='juz',
            name='start_verse',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='juz',
            name='surah',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='juz', to='islam.surah1'),
        ),
        migrations.AlterField(
            model_name='surah1',
            name='count',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='surah1',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='surah1',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verse_number', models.PositiveIntegerField()),
                ('verse_ar', models.TextField(blank=True, null=True)),
                ('verse_en', models.TextField(blank=True, null=True)),
                ('surah', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verses', to='islam.surah1')),
            ],
            options={
                'ordering': ['verse_number'],
                'unique_together': {('surah', 'verse_number')},
            },
        ),
    ]