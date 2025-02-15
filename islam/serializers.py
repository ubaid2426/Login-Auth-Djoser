from rest_framework import serializers
from .models import DuaCard, EventCard, HadithCard, HolyPlace, HolyPlaceImage, Surah, Surah1, Verse, Juz, NameAllah, Hadith, Metadata, VerseCard

class SurahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Surah
        fields = '__all__'


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ["verse_number", "verse_ar", "verse_en"]


class JuzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Juz
        fields = ["index", "start_verse", "end_verse"]


class Surah1Serializer(serializers.ModelSerializer):
    verse_ar = serializers.SerializerMethodField()
    verse_en = serializers.SerializerMethodField()
    juz = serializers.SerializerMethodField()

    class Meta:
        model = Surah1
        fields = ["index", "name", "count", "verse_ar", "verse_en", "juz"]

    def get_verse_ar(self, obj):
        return {f"verse_{verse.verse_number}": verse.verse_ar for verse in obj.verses.all()}

    def get_verse_en(self, obj):
        return {f"verse_{verse.verse_number}": verse.verse_en for verse in obj.verses.all()}

    def get_juz(self, obj):
        return [
            {
                "index": j.index,
                "verse": {"start": j.start_verse, "end": j.end_verse}
            }
            for j in obj.juz.all()
        ]



class NameAllahSerializer(serializers.ModelSerializer):
    class Meta:
        model = NameAllah
        fields = ['id', 'eng_name', 'icon', 'eng_meaning', 'explanation']


class HadithSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hadith
        fields = '__all__'


class MetadataSerializer(serializers.ModelSerializer):
    hadiths = HadithSerializer(many=True, read_only=True)

    class Meta:
        model = Metadata
        fields = '__all__'


class VerseCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerseCard
        fields = ['id', 'reference', 'arabic_text', 'urdu_text']
        extra_kwargs = {
            'reference': {'required': True},
            'arabic_text': {'required': True},
            'urdu_text': {'required': True},
        }

class HolyPlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolyPlaceImage
        fields = ['id', 'image']

class HolyPlaceSerializer(serializers.ModelSerializer):
    images = HolyPlaceImageSerializer(many=True, read_only=True)  # Multiple images
    cover_image = serializers.ImageField(required=False)  # Single image

    class Meta:
        model = HolyPlace
        fields = ['id', 'title', 'description', 'category', 'cover_image', 'latitude', 'longitude', 'country', 'city', 'area', 'images']

        
class DuaCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuaCard
        fields = ['id', 'reference', 'dua', 'arabic_text', 'urdu_text']
        extra_kwargs = {
            'reference': {'required': True},
            'dua': {'required': True},
            'arabic_text': {'required': True},
            'urdu_text': {'required': True},
        }

class HadithCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HadithCard
        fields = ['id', 'reference', 'urdu_text']
        extra_kwargs = {
            'reference': {'required': True},
            'urdu_text': {'required': True},
        }

class EventCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCard
        fields = ['id', 'urdu_text']
        extra_kwargs = {
            'urdu_text': {'required': True},
        }