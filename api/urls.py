from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

from api.views import (
    note_detail_update_delete_api_view,
    note_list_create_api_view,
)

app_name = 'api'

urlpatterns = [
    path('notes/', note_list_create_api_view, name='list'),
    path('notes/<int:pk>/', note_detail_update_delete_api_view, name='detail'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
