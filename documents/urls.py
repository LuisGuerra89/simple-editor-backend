from django.urls import path
from .views import get_document, save_document

urlpatterns = [
    path('document/', get_document, name='get_document'),
    path('document/save/', save_document, name='save_document'),
]
