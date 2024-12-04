from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.conf.urls import handler404, handler403
from .forms import LoginForm, RegistroUsuarioForm
from .models import Ticket, Encuesta
from django.db import IntegrityError
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

def index_vista(request):
    return render(request, 'index.html')

# Decorador para verificar si el usuario es staff
def is_staff_user(user):
    if user.is_staff:
        return True
    raise PermissionDenied

# ---- Vistas de Autenticación ----
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Bienvenido {user.first_name or user.username}.")
                    return redirect('home')
                messages.error(request, "Correo o contraseña incorrectos.")
            except CustomUser.DoesNotExist:
                messages.error(request, "Correo no registrado.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def custom_logout(request):
    logout(request)
    return redirect('login')

def registrarse_vista(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, "Tu cuenta ha sido creada exitosamente.")
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registrarse.html', {'usuario_form': form})

# ---- Vistas de Usuario ----
@login_required
def perfil_usuario(request):
    return render(request, 'perfil.html', {'user': request.user})

@login_required
def home_vista(request):
    context = {
        "tickets_total": Ticket.objects.count(),
        "tickets_pendientes": Ticket.objects.filter(estado="Pendiente").count(),
        "tickets_resueltos": Ticket.objects.filter(estado="Resuelto").count(),
        "tickets_en_proceso": Ticket.objects.filter(estado="En Progreso").count(),
        "tickets_recientes": Ticket.objects.order_by("-fecha_creacion")[:5],
    }
    return render(request, "home.html", context)

# ---- Vistas de Tickets ----
@login_required
def ticket_vista(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        if not (titulo and descripcion):
            messages.error(request, "El título y la descripción son obligatorios.")
        else:
            Ticket.objects.create(titulo=titulo, descripcion=descripcion, usuario=request.user)
            messages.success(request, "El ticket fue creado exitosamente.")
            return redirect("home")
    return render(request, "ticket1.html")

@login_required
@user_passes_test(is_staff_user)
def dashboard_vista(request):
    context = {
        'tickets_pendientes': Ticket.objects.filter(estado="Pendiente").count(),
        'tickets_en_proceso': Ticket.objects.filter(estado="En Progreso").count(),
        'tickets_resueltos': Ticket.objects.filter(estado="Resuelto").count(),
        'tickets_por_mes': (
            Ticket.objects.annotate(mes=TruncMonth('fecha_creacion'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        ),
        'tickets_por_tecnico': (
            Ticket.objects.values('tecnico_asignado__first_name', 'tecnico_asignado__last_name')
            .annotate(total=Count('id'))
            .order_by('-total')
        ),
        'tickets_por_empresa': (
            Ticket.objects.values('usuario__nombre_empresa')
            .annotate(total=Count('id'))
            .order_by('-total')
        ),
    }
    return render(request, 'dashboard.html', context)

@login_required
def detalle_ticket_vista(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST' and request.user.is_staff:
        ticket.estado = request.POST.get('estado')
        ticket.prioridad = request.POST.get('prioridad')
        ticket.solucion = request.POST.get('solucion')
        ticket.visita_terreno = 'visita_terreno' in request.POST
        if ticket.estado == 'En Progreso' and ticket.tecnico_asignado is None:
            ticket.tecnico_asignado = request.user
        ticket.save()
        messages.success(request, "El ticket ha sido actualizado correctamente.")
        return redirect('dashboard')
    return render(request, 'detalle_ticket.html', {'ticket': ticket})

@login_required
def eliminar_ticket_vista(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()
        messages.success(request, "El ticket ha sido eliminado exitosamente.")
    except Ticket.DoesNotExist:
        messages.error(request, "El ticket no existe.")
    return redirect('dashboard')

@login_required
def encuesta_vista(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not request.user.is_staff and ticket.estado == "Resuelto":
        if request.method == "POST":
            Encuesta.objects.create(
                ticket=ticket,
                calificacion=request.POST.get("rating"),
                comentarios=request.POST.get("comments"),
            )
            messages.success(request, "¡Gracias por calificar el servicio!")
            return redirect("home")
        return render(request, "encuesta.html", {"ticket": ticket})
    messages.error(request, "No tienes permiso para calificar este ticket.")
    return redirect("home")

# ---- Manejo de Errores ----
def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)

