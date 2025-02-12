from django.contrib import admin
from .models import DuaCard, EventCard, HadithCard, HolyPlace, HolyPlaceImage, Surah, Surah1, Verse, Juz, NameAllah, Hadith, Metadata, VerseCard

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
@admin.register(VerseCard)
class VerseCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'arabic_text', 'urdu_text')
    # search_fields = ('reference', 'arabic_text', 'urdu_text')
class HolyPlaceImageInline(admin.TabularInline):
    model = HolyPlaceImage
    extra = 1  # Allows adding multiple images at once
    
@admin.register(DuaCard)
class DuaCardAdmin(admin.ModelAdmin):
    list_display = ('reference', 'dua', 'arabic_text', 'urdu_text')
    # search_fields = ('reference', 'dua', 'arabic_text', 'urdu_text')
@admin.register(HolyPlace)
class HolyPlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'country', 'city', 'area', 'cover_image', 'latitude', 'longitude']
    search_fields = ['title', 'description', 'category', 'country', 'city', 'area']
    list_filter = ['country', 'city', 'area', 'category']
    inlines = [HolyPlaceImageInline]  # Inline multiple images

@admin.register(HolyPlaceImage)
class HolyPlaceImageAdmin(admin.ModelAdmin):
    list_display = ['holy_place', 'image']

@admin.register(HadithCard)
class HadithCardAdmin(admin.ModelAdmin):
    list_display = ('reference', 'urdu_text')
    # search_fields = ('reference', 'urdu_text')

@admin.register(EventCard)
class EventCardAdmin(admin.ModelAdmin):
    list_display = ['urdu_text']
    # search_fields = ('urdu_text')

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