from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Document
from docx import Document as DocxDocument
import os
import json

# Vista para leer el documento
def get_document(request):
    # Si no tenemos documentos guardados, devolvemos un contenido por defecto
    document = Document.objects.first()
    if document:
        content = document.content
    else:
        content = "Texto inicial del documento desde la API."
    return JsonResponse({"content": content})

# Vista para guardar el documento
@csrf_exempt
def save_document(request):
    if request.method == 'POST':
        try:
            # Cargar el cuerpo de la solicitud como JSON
            data = json.loads(request.body)
            content = data.get('content', '')

            # Guardamos el contenido en un modelo de Document
            document, _ = Document.objects.get_or_create(id=1)
            document.content = content
            document.save()

            # Creamos un archivo .docx con el contenido recibido
            doc = DocxDocument()
            doc.add_paragraph(content)
            file_path = os.path.join(os.getcwd(), 'output.docx')
            doc.save(file_path)

            return JsonResponse({'message': f'Document saved as {file_path}'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
