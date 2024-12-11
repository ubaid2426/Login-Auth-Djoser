import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Surah, Surah1, Verse, Juz, NameAllah, Hadith, Metadata
from .serializers import SurahSerializer, Surah1Serializer, NameAllahSerializer, MetadataSerializer

class SurahListView(APIView):
    def get(self, request):
        surahs = Surah.objects.all()
        serializer = SurahSerializer(surahs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SurahSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Surah1DetailView(APIView):
    def get(self, request, index):
        try:
            surah = Surah1.objects.get(index=index)
            serializer = Surah1Serializer(surah)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Surah1.DoesNotExist:
            return Response(
                {
                    "error": "Surah not found",
                    "details": f"No Surah1 found with index {index}. Check the database."
                },
                status=status.HTTP_404_NOT_FOUND
            )



    def post(self, request, index):
        try:
            # Fetch or create the Surah1 object
            surah, created = Surah1.objects.get_or_create(
                index=index,
                defaults={
                    "name": request.data.get("name"),
                    "count": request.data.get("count", 0)
                }
            )

            # Save or update Verse data
            verse_ar = request.data.get("verse_ar", {})
            verse_en = request.data.get("verse_en", {})
            for verse_key, verse_text in verse_ar.items():
                verse_number = int(verse_key.split("_")[1])  # Extract verse number from "verse_1"
                Verse.objects.update_or_create(
                    surah=surah,
                    verse_number=verse_number,
                    defaults={
                        "verse_ar": verse_text,
                        "verse_en": verse_en.get(verse_key, "")  # Use empty string if no matching verse in verse_en
                    }
                )

            # Save Juz data
            juz_data = request.data.get("juz", [])
            for juz_item in juz_data:
                Juz.objects.update_or_create(
                    surah=surah,
                    index=juz_item["index"],
                    defaults={
                        "start_verse": juz_item["verse"]["start"],
                        "end_verse": juz_item["verse"]["end"],
                    }
                )

            return Response({"message": "Surah data created/updated successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NameAllahList(APIView):
    def get(self, request):
        names = NameAllah.objects.all()
        serializer = NameAllahSerializer(names, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Use 'many=True' to handle a list of Surahs in the request data
        serializer = NameAllahSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









# List all Hadith or create new ones
class UploadHadithData(APIView):
    def post(self, request, *args, **kwargs):
        # Load JSON from request
        try:
            data = json.loads(request.body)

            # Handle metadata (save only once)
            metadata_data = data.get("metadata", {})
            metadata, created = Metadata.objects.get_or_create(
                arabic_title=metadata_data.get("arabic", {}).get("title"),
                length=metadata_data.get("length"),
                arabic_author=metadata_data.get("arabic", {}).get("author"),
                arabic_introduction=metadata_data.get("arabic", {}).get("introduction"),
                english_title=metadata_data.get("english", {}).get("title"),
                english_author=metadata_data.get("english", {}).get("author"),
                english_introduction=metadata_data.get("english", {}).get("introduction"),
            )

            # Handle hadiths
            hadiths_data = data.get("hadiths", [])
            for hadith in hadiths_data:
                Hadith.objects.create(
                    metadata=metadata,
                    hadith_id=hadith.get("id"),
                    id_in_book=hadith.get("idInBook"),
                    chapter_id=hadith.get("chapterId"),
                    book_id=hadith.get("bookId"),
                    arabic_hadith=hadith.get("arabic"),
                    english_narrator=hadith.get("english", {}).get("narrator"),
                    english_text=hadith.get("english", {}).get("text"),
                )

            return Response({"message": "Data successfully uploaded."})

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    def get(self, request, *args, **kwargs):
        try:
            # Retrieve all metadata with their related hadiths
            metadata = Metadata.objects.all()
            serializer = MetadataSerializer(metadata, many=True)

            return Response(serializer.data)

        except Exception as e:
            return Response({"error": str(e)}, status=400)