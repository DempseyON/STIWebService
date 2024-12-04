from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from STIWEBSERVICE import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_vista, name='index'),
    path('ticket/', views.ticket_vista, name='ticket'),
    path('registrarse/', views.registrarse_vista, name='registrarse'),
    path('dashboard/', views.dashboard_vista, name='dashboard'),
    path('paneladmin/', views.paneladmin_vista, name='paneladmin'),
    path('ticket/<int:ticket_id>/asignar/',
         views.asignarticket_vista,
         name='asignarticket'),
    path('ticket/<int:ticket_id>/',
         views.detalleticket_vista,
         name='detalleticket'),
    path('ticket/<int:ticket_id>/editar/',
         views.edicionticket_vista,
         name='edicionticket'),
    path('historialticket/',
         views.historialticket_vista,
         name='historialticket'),
    path('loginadmin/', views.loginadmin_vista, name='loginadmin'),
    path('configuracionusuario/',
         views.configuracionusuario_vista,
         name='configuracionusuario'),
    path('encuesta/<int:ticket_id>', views.encuesta_vista, name='encuesta'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('confirmar-cerrar-sesion/',
         views.confirmar_logout,
         name='confirmar_logout'),
    path('logout/', views.custom_logout, name='logout'),
]
