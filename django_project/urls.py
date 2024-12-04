from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, re_path

from STIWEBSERVICE import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_vista, name='index'),
    path('ticket/', views.ticket_vista, name='ticket'),
    path('registrarse/', views.registrarse_vista, name='registrarse'),
    path('home/', views.home_vista, name='home'),
    path('ticket/<int:ticket_id>/',
         views.detalle_ticket_vista, name='detalleticket'),
    path('ticket/eliminar/<int:ticket_id>/',
         views.eliminar_ticket_vista, name='eliminar_ticket'),

    path('dashboard/', views.dashboard_vista, name='dashboard'),
    path('encuesta/<int:ticket_id>', views.encuesta_vista, name='encuesta'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('logout/', views.custom_logout, name='logout'),
    re_path(r'^.*$', views.error_404_view, name='error_404'),
]
