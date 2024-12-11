from django.contrib import admin
from .models import Surah, Surah1, Verse, Juz, NameAllah, Hadith, Metadata

@admin.register(Surah)
class SurahAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'transliteration', 'translation', 'type', 'total_verses')
    list_filter = ('type',)
    search_fields = ('name', 'transliteration', 'translation')
    ordering = ('id',)


class VerseInline(admin.TabularInline):
    model = Verse
    fields = ("verse_number", "verse_ar", "verse_en")
    extra = 1


class JuzInline(admin.TabularInline):
    model = Juz
    fields = ("index", "start_verse", "end_verse")
    extra = 1


@admin.register(Surah1)
class Surah1Admin(admin.ModelAdmin):
    list_display = ("index", "name", "count")
    inlines = [VerseInline, JuzInline]


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ("surah", "verse_number", "verse_ar", "verse_en")
    list_filter = ("surah",)


@admin.register(Juz)
class JuzAdmin(admin.ModelAdmin):
    list_display = ("index", "surah", "start_verse", "end_verse")

@admin.register(NameAllah)
class NameAllahAdmin(admin.ModelAdmin):
    list_display = ("id", "eng_name", "icon")
    # list_filter = ("id")


@admin.register(Metadata)
class MetadataAdmin(admin.ModelAdmin):
    list_display = ('english_title', 'arabic_title', 'english_author')
    search_fields = ('english_title', 'arabic_title', 'english_author')

@admin.register(Hadith)
class HadithAdmin(admin.ModelAdmin):
    list_display = ('hadith_id', 'chapter_id', 'book_id', 'english_narrator')
    search_fields = ('hadith_id', 'english_narrator')