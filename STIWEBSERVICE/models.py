from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class CustomUser(AbstractUser):
    nombre_empresa = models.CharField(max_length=255, blank=True, null=True)
    cargo = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username

    def clean(self):
        if not self.nombre_empresa:
            raise ValidationError("El nombre de la empresa es obligatorio.")




@receiver(post_save, sender=CustomUser)
def asignar_empresa_automatica(sender, instance, created, **kwargs):
    if created and not instance.nombre_empresa:
        email = instance.email
        dominio = email.split('@')[1].split('.')[0]  # Extrae el dominio
        instance.nombre_empresa = dominio.upper()  # Convertir el dominio en mayúsculas
        instance.save()




class Ticket(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Progreso', 'En Progreso'),
        ('Resuelto', 'Resuelto'),
    ]
    PRIORIDAD_CHOICES = [
        ('Alta', 'Alta'),
        ('Media', 'Media'),
        ('Baja', 'Baja'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='tickets')
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    prioridad = models.CharField(
        max_length=20, choices=PRIORIDAD_CHOICES, default='Media', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    tecnico_asignado = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, related_name='tickets_asignados_tecnico', blank=True, null=True)
    visita_terreno = models.BooleanField(default=False)
    solucion = models.TextField(blank=True, null=True)  


    def __str__(self):
        return f"Ticket #{self.id} - {self.titulo}"


class Comentario(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario por {self.usuario.username} en Ticket #{self.ticket.id}"


class Encuesta(models.Model):
    ticket = models.OneToOneField(
        Ticket, on_delete=models.CASCADE, related_name="encuesta")
    calificacion = models.PositiveSmallIntegerField()  # 1 a 5 estrellas
    comentarios = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta para Ticket #{self.ticket.id} - Calificación: {self.calificacion}"

class RegistroErrores(models.Model):
    tipo_error = models.CharField(max_length=50)  # Ejemplo: '404', '500'
    descripcion = models.TextField()
    fecha_ocurrencia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Error {self.tipo_error} - {self.fecha_ocurrencia}"
