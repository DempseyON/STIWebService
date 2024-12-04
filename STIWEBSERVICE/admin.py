from django.contrib import admin
from .models import Departamento, Ticket, Comentario, Asignacion, Encuesta, RegistroErrores

admin.site.register(Departamento)
admin.site.register(Ticket)
admin.site.register(Comentario)
admin.site.register(Asignacion)
admin.site.register(Encuesta)
admin.site.register(RegistroErrores)
