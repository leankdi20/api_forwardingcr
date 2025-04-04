from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import EmailValidator

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'usuario@costaricaforwarding.com'
        }),
        label="Correo electrónico",
        validators=[EmailValidator(message="Ingrese un correo válido.")],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        label="Contraseña",
    )