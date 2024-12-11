from django.db import models

class Surah(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    transliteration = models.CharField(max_length=255)
    translation = models.CharField(max_length=255)
    type = models.CharField(max_length=50)
    total_verses = models.IntegerField()

    def __str__(self):
        return self.name


class Surah1(models.Model):
    index = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.index} - {self.name}"


class Verse(models.Model):
    surah = models.ForeignKey(Surah1, on_delete=models.CASCADE, related_name="verses")
    verse_number = models.PositiveIntegerField()
    verse_ar = models.TextField(null=True)
    verse_en = models.TextField(null=True)

    def __str__(self):
        return f"{self.surah.name} - Verse {self.verse_number}"


class Juz(models.Model):
    surah = models.ForeignKey(Surah1, on_delete=models.CASCADE, related_name="juz")
    index = models.CharField(max_length=10)
    start_verse = models.CharField(max_length=20)
    end_verse = models.CharField(max_length=20)

    def __str__(self):
        return f"Juz {self.index} - Surah {self.surah.name}"


class NameAllah(models.Model):
    id = models.IntegerField(primary_key=True)
    eng_name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='imgs/', null=True, blank=True)
    eng_meaning = models.CharField(max_length=255)
    explanation = models.TextField()

    def __str__(self):
        return self.eng_name









class Metadata(models.Model):
    length = models.CharField(max_length=2555, null=True)
    arabic_title = models.CharField(max_length=2555)
    arabic_author = models.CharField(max_length=2555)
    arabic_introduction = models.TextField()
    english_title = models.CharField(max_length=2555)
    english_author = models.CharField(max_length=2555)
    english_introduction = models.TextField()
    
    def __str__(self):
        return f"Metadata: {self.english_title}"


class Hadith(models.Model):
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE, related_name="hadiths", null=True)
    hadith_id = models.IntegerField()
    id_in_book = models.IntegerField()
    chapter_id = models.IntegerField()
    book_id = models.IntegerField()
    arabic_hadith = models.TextField()
    english_narrator = models.CharField(max_length=2555)
    english_text = models.TextField()

    def __str__(self):
        return f"Hadith {self.hadith_id}"