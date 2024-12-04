from django import forms
from django.contrib.auth.models import User

from .models import PerfilUsuario


class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")


class PerfilUsuarioForm(forms.ModelForm):

    class Meta:
        model = PerfilUsuario
        fields = ['nombre_empresa', 'cargo']
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico'
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        }))
