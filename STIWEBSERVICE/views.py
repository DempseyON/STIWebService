from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render

from .forms import LoginForm, PerfilUsuarioForm, RegistroUsuarioForm
from .models import (
    Departamento,
    PerfilUsuario,
    Ticket,
)


def custom_logout(request):
    logout(request)
    return redirect('login')


# Create your views here.
def index_vista(request):
    return render(request, 'index.html')


@login_required
def confirmar_logout(request):
    return render(request, 'cerrar_sesion.html')


@login_required
def perfil_usuario(request):
    return render(request, 'perfil.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(
                request, username=email,
                password=password)  # Usamos el email como username
            if user is not None:
                login(request, user)
                messages.success(
                    request, f"Bienvenido {user.first_name or user.username}.")
                return redirect(
                    'dashboard')  # Redirige al dashboard o página principal
            else:
                messages.error(request, "Correo o contraseña incorrectos.")
    else:
        form = LoginForm()

    # Renderiza la plantilla de login
    return render(request, 'login.html', {'form': form})


def ticket_vista(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        departamento_id = request.POST.get("departamento")
        prioridad = request.POST.get("prioridad")

        # Validación de datos
        if not (titulo and descripcion and departamento_id and prioridad):
            messages.error(request, "Todos los campos son obligatorios.")
        else:
            # Crear el ticket
            departamento = Departamento.objects.get(id=departamento_id)
            Ticket.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                departamento=departamento,
                prioridad=prioridad,
                usuario=request.user  # Usuario autenticado
            )
            messages.success(request, "El ticket fue creado exitosamente.")
            return redirect("dashboard")

    departamentos = Departamento.objects.all()
    return render(request, "ticket1.html", {"departamentos": departamentos})


def registrarse_vista(request):
    if request.method == 'POST':
        usuario_form = RegistroUsuarioForm(request.POST)
        perfil_form = PerfilUsuarioForm(request.POST)

        if usuario_form.is_valid() and perfil_form.is_valid():
            try:
                # Guardar el usuario
                usuario = usuario_form.save(commit=False)
                usuario.set_password(usuario_form.cleaned_data['password'])
                usuario.save()

                # Verificar si el perfil ya existe
                if not PerfilUsuario.objects.filter(usuario=usuario).exists():
                    # Guardar el perfil asociado
                    perfil = perfil_form.save(commit=False)
                    perfil.usuario = usuario
                    perfil.save()
                    messages.success(request,
                                     "Tu cuenta ha sido creada exitosamente.")
                else:
                    messages.error(request,
                                   "El perfil para este usuario ya existe.")
                return redirect(
                    'login')  # Redirigir al login después del registro

            except IntegrityError:
                messages.error(
                    request,
                    "Ocurrió un error al registrar tu cuenta. Por favor intenta de nuevo."
                )
        else:
            messages.error(request,
                           "Por favor corrige los errores en el formulario.")
    else:
        usuario_form = RegistroUsuarioForm()
        perfil_form = PerfilUsuarioForm()

    return render(request, 'registrarse.html', {
        'usuario_form': usuario_form,
        'perfil_form': perfil_form
    })


@login_required
def dashboard_vista(request):
    tickets_total = Ticket.objects.count()
    tickets_pendientes = Ticket.objects.filter(estado="Pendiente").count()
    tickets_resueltos = Ticket.objects.filter(estado="Resuelto").count()
    tickets_sin_asignar = Ticket.objects.filter(
        asignacion__isnull=True).count()

    tickets_recientes = Ticket.objects.order_by("-fecha_creacion")[:5]

    context = {
        "tickets_total": tickets_total,
        "tickets_pendientes": tickets_pendientes,
        "tickets_resueltos": tickets_resueltos,
        "tickets_sin_asignar": tickets_sin_asignar,
        "tickets_recientes": tickets_recientes,
    }
    return render(request, "dashboard.html", context)


def paneladmin_vista(request):
    return render(request, 'panel_admin.html')


def asignarticket_vista(request):
    return render(request, 'asignar_ticket.html')


def detalleticket_vista(request):
    return render(request, 'detalle_ticket.html')


def edicionticket_vista(request):
    return render(request, 'edicion_ticket.html')


def historialticket_vista(request):
    return render(request, 'historial_ticket.html')


def loginadmin_vista(request):
    return render(request, 'login_admin.html')


def configuracionusuario_vista(request):
    return render(request, 'configuracion_usuario.html')


def encuesta_vista(request):
    return render(request, 'encuesta.html')
