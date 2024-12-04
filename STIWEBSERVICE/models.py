from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
  if created:
    PerfilUsuario.objects.create(usuario=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
  instance.perfil.save()


class PerfilUsuario(models.Model):
  usuario = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 related_name="perfil")
  nombre_empresa = models.CharField(max_length=200)
  cargo = models.CharField(max_length=200)

  def __str__(self):
    return f"{self.usuario.username} - {self.nombre_empresa} ({self.cargo})"


class Departamento(models.Model):
  """
    Modelo para representar departamentos donde se asignan tickets.
    """
  nombre = models.CharField(max_length=100, unique=True)

  def __str__(self):
    return self.nombre


class Ticket(models.Model):
  """
    Modelo para representar los tickets de soporte.
    """
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
  usuario = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='tickets')

  estado = models.CharField(max_length=20,
                            choices=ESTADO_CHOICES,
                            default='Pendiente')
  prioridad = models.CharField(max_length=20,
                               choices=PRIORIDAD_CHOICES,
                               default='Media')
  fecha_creacion = models.DateTimeField(auto_now_add=True)
  fecha_actualizacion = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"Ticket #{self.id} - {self.titulo}"


class Comentario(models.Model):
  """
    Modelo para representar comentarios dentro de un ticket.
    """
  ticket = models.ForeignKey(Ticket,
                             on_delete=models.CASCADE,
                             related_name='comentarios')
  usuario = models.ForeignKey(User, on_delete=models.CASCADE)
  contenido = models.TextField()
  fecha_creacion = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Comentario por {self.usuario.username} en Ticket #{self.ticket.id}"


class Asignacion(models.Model):
  """
    Modelo para representar la asignación de un ticket a un técnico.
    """
  ticket = models.OneToOneField(Ticket,
                                on_delete=models.CASCADE,
                                related_name='asignacion')
  asignado_a = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='tickets_asignados')
  fecha_asignacion = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Ticket #{self.ticket.id} asignado a {self.asignado_a.username}"


class Encuesta(models.Model):
  """
    Modelo para representar encuestas de satisfacción sobre tickets resueltos.
    """
  ticket = models.OneToOneField(Ticket,
                                on_delete=models.CASCADE,
                                related_name='encuesta')
  calificacion = models.PositiveSmallIntegerField()  # 1 a 5 estrellas
  comentarios = models.TextField(blank=True, null=True)
  fecha_creacion = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Encuesta para Ticket #{self.ticket.id} - Calificación: {self.calificacion}"


class RegistroErrores(models.Model):
  """
    Modelo para registrar errores 404 o 500.
    """
  tipo_error = models.CharField(max_length=50)  # Ejemplo: '404', '500'
  descripcion = models.TextField()
  fecha_ocurrencia = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Error {self.tipo_error} - {self.fecha_ocurrencia}"
