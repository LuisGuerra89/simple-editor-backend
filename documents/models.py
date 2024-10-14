from django.db import models

class Document(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento {self.id} - Creado el {self.created_at}"

# Create your models here.
