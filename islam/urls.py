from django.urls import path
from .views import SurahListView, Surah1DetailView, NameAllahList, UploadHadithData

urlpatterns = [
    path('surah/', SurahListView.as_view(), name='surah-list'),
    path("surah-detail/<str:index>/", Surah1DetailView.as_view(), name="surah-detail"),
    path('name-allah/', NameAllahList.as_view(), name='surah-list'),
    path('upload-hadith-data/', UploadHadithData.as_view(), name='upload-hadith-data'),
]
