from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from api.views import (
    # functions views
    note_detail_update_delete_api_view,
    note_list_create_api_view,

    # APIView
    NoteListAPIView,
    NoteDetailAPIView,

    # APIView with mixins
    NoteListCreateAPIView,
    NoteDetailUpdateDeleteAPIView,
    EasyNoteListCreateAPIView,
    EasyNoteDetailUpdateDeleteAPIView,

    # ModelViewSet
    NoteModelViewSet,
)

app_name = 'api'

# notes_LIST = NoteModelViewSet.as_view(
#     {
#         'get': 'list',  # соответсвия между методами HTTP и действиями ViewSet
#         'post': 'create',
#     }
# )
# notes_DETAIL = NoteModelViewSet.as_view(
#     {
#         'get': 'retrieve',
#         'put': 'update',
#         'patch': 'partial_update',
#         'delete': 'destroy',
#     }
# )
# urlpatterns = [
#     path('notes/', notes_LIST, name='notes-list'),
#     path('notes/<int:pk>/', notes_DETAIL, name='notes-detail'),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)
router = DefaultRouter()
router.register(
    prefix='notes',
    viewset=NoteModelViewSet,
    basename='notes'
)
urlpatterns = router.urls
