from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from docx import Document as DocxDocument
import os
import json

def list_documents(request):
    documents = Document.objects.all()
    document_list = [{'id': doc.id, 'content': doc.content} for doc in documents]
    return JsonResponse(document_list, safe=False)


def get_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return JsonResponse({"id": document.id, "content": document.content})


@csrf_exempt
def save_document(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '')
            document_id = data.get('id', None)

            if document_id:
                document = get_object_or_404(Document, id=document_id)
                document.content = content
                document.save()
                message = 'Document updated'
            else:
                document = Document.objects.create(content=content)
                message = 'Document created'

            doc = DocxDocument()
            doc.add_paragraph(content)
            file_path = os.path.join(os.getcwd(), f'output_{document.id}.docx')
            doc.save(file_path)

            return JsonResponse({'message': f'{message} as {file_path}'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_document(request, id):
    if request.method == 'DELETE':
        try:
            document = get_object_or_404(Document, id=id)
            document.delete()
            return JsonResponse({'message': 'Document deleted successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)