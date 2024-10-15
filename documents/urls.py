from django.urls import path
from .views import get_document, save_document, list_documents, delete_document

urlpatterns = [
    path('document/list/', list_documents, name='list_documents'),

    path('document/<int:document_id>/', get_document, name='get_document'),

    path('document/save/', save_document, name='save_document'),

    path('document/delete/<int:id>/', delete_document, name='delete_document'),
]
