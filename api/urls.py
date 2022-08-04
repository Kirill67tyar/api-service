from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from api.views import (
    note_detail_update_delete_api_view,
    note_list_create_api_view,
    NoteListAPIView,
    NoteDetailAPIView,
    NoteListCreateAPIView,
    NoteDetailUpdateDeleteAPIView,
    EasyNoteListCreateAPIView,
    EasyNoteDetailUpdateDeleteAPIView,
)

app_name = 'api'

urlpatterns = [
    path('notes/', EasyNoteListCreateAPIView.as_view(), name='list'),
    path('notes/<int:pk>/', EasyNoteDetailUpdateDeleteAPIView.as_view(), name='detail'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
