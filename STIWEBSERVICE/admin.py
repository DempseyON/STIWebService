from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import PermissionDenied
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Campos que se muestran en la página de detalles del usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'nombre_empresa', 'cargo')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    # Campos que se muestran al crear un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        # Restringir cambios de `is_staff` a superusuarios
        if not request.user.is_superuser and 'is_staff' in form.changed_data:
            raise PermissionDenied("Solo los superusuarios pueden modificar el estado de 'is_staff'.")
        super().save_model(request, obj, form, change)

# Registrar el modelo en el admin
admin.site.register(CustomUser, CustomUserAdmin)