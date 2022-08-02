from django.urls import path

from notes.views import analyze_view

app_name = 'notes'

urlpatterns = [
    path('analyze/', analyze_view, name='analyze'),
]
