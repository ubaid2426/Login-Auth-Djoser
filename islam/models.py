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
class VerseCard(models.Model):
    reference = models.TextField()  # Unique reference field
    arabic_text = models.TextField()  # Arabic text
    urdu_text = models.TextField() # Urdu text

    def __str__(self):
        return self.reference
    

class DuaCard(models.Model):
    reference = models.TextField()  # Unique reference field
    arabic_text = models.TextField()  # Arabic text
    dua = models.TextField()  # Arabic text
    urdu_text = models.TextField()  # Urdu text

    def __str__(self):
        return self.reference



class Category(models.Model):
    title = models.CharField(max_length=255)  # Title of the category

    def __str__(self):
        return self.title  # Return the title as the string representation
    

def get_default_category():
    return Category.objects.get_or_create(title="Uncategorized")[0].id    
class HolyPlace(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='holy_places/', null=True, blank=True)  # Single image
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    # category=models.CharField(max_length=100, null=True, blank=True)   #holyplace and site
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='donations', default=get_default_category)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.title


class HolyPlaceImage(models.Model):
    holy_place = models.ForeignKey(HolyPlace, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='holy_places/')

    def __str__(self):
        return f"Image for {self.holy_place.title}"

class HadithCard(models.Model):
    reference = models.TextField()  # Unique reference field
    # arabic_text = models.CharField(max_length=255)  # Arabic text
    urdu_text = models.TextField()  # Urdu text

    def __str__(self):
        return self.reference
    

class EventCard(models.Model):
    urdu_text = models.TextField()  # Urdu text

    def __str__(self):
        return self.urdu_text
    


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
    length = models.TextField(null=True)
    arabic_title = models.TextField()
    arabic_author = models.TextField()
    arabic_introduction = models.TextField()
    english_title = models.TextField()
    english_author = models.TextField()
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
    english_narrator = models.TextField()
    english_text = models.TextField()

    def __str__(self):
        return f"Hadith {self.hadith_id}"