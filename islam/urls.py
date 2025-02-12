from django.urls import path
from .views import DuaCardListCreateView, DuaCardRetrieveUpdateView, EventCardListCreateView, EventCardRetrieveUpdateView, HadithCardListCreateView, HadithCardRetrieveUpdateView, HolyPlaceViewSet, SurahListView, Surah1DetailView, NameAllahList, UploadHadithData, VerseCardListCreateView, VerseCardRetrieveUpdateView

urlpatterns = [
    path('surah/', SurahListView.as_view(), name='surah-list'),
    path("surah-detail/<str:index>/", Surah1DetailView.as_view(), name="surah-detail"),
    path('name-allah/', NameAllahList.as_view(), name='surah-list'),
    path('upload-hadith-data/', UploadHadithData.as_view(), name='upload-hadith-data'),
    path('VerseCard/', VerseCardListCreateView.as_view(), name='translation-list-create'),
    path('VerseCard/<int:pk>/', VerseCardRetrieveUpdateView.as_view(), name='translation-retrieve-update'),
    path('HadithCard/', HadithCardListCreateView.as_view(), name='Hadith-list-create'),
    path('HadithCard/<int:pk>/', HadithCardRetrieveUpdateView.as_view(), name='Hadith-retrieve-update'),
    path('EventCard/', EventCardListCreateView.as_view(), name='Event-list-create'),
    path('EventCard/<int:pk>/', EventCardRetrieveUpdateView.as_view(), name='Event-retrieve-update'),
    path('DuaCard/', DuaCardListCreateView.as_view(), name='Dua-list-create'),
    path('DuaCard/<int:pk>/', DuaCardRetrieveUpdateView.as_view(), name='Dua-retrieve-update'),
        path('holyplaces/', HolyPlaceViewSet.as_view({'get': 'list', 'post': 'create'}), name='holyplace-list-create'),
    path('holyplaces/<int:pk>/', HolyPlaceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='holyplace-detail'),
    # path('holyplaces/', HolyPlaceViewSet.as_view({'get': 'list', 'post': 'create'}), name='holyplace-list-create'),
    # path('holyplaces/<int:pk>/', HolyPlaceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='holyplace-detail'),
]
