from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


import random


from .forms import LoginForm

# Diccionario temporal para almacenar códigos de seguridad
security_codes = {}

def login_view(request):
    """ Vista de Login con validaciones corregidas """
    
    if request.user.is_authenticated:
        return redirect("base")  # Evita que un usuario ya autenticado vea el login
    
    # Si el usuario regresa desde "base" con Back, cerramos sesión
    if "base" in request.META.get("HTTP_REFERER", ""):
        logout(request)
    
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # Usa el formulario con validaciones

        if form.is_valid():
            email = form.cleaned_data["username"]  # Ahora `username` es un email
            password = form.cleaned_data["password"]

            user = authenticate(request, username=email, password=password)  # Verificar con `email`
            if user:
                #Generar un código de 2 dígitos de forma random
                code = random.randint(10, 9999)
                security_codes[email] = code 
                
                send_verification_email(email, user.first_name, code)

                #Guarda el email en la sesión y redirige a la pagina de verificación
                request.session['pending_email'] = email
                return redirect("verify_code")
            else:
                form.add_error(None, "Correo o contraseña incorrectos.")

    else:
        form = LoginForm()

    return render(request, "core/login.html", {"form": form})


def verify_code_view(request):
    """ Vista para ingresar el código de seguridad """
    
    pending_email = request.session.get("pending_email")

    if not pending_email:
        return redirect("login")  # Si no hay email en la sesión, redirigir al login

    if request.method == "POST":
        entered_code = request.POST.get("code")

        # Validar si el código existe para este correo
        if entered_code and pending_email in security_codes:
            try:
                if int(entered_code) == security_codes[pending_email]:
                    # Obtener el usuario autenticado
                    User = get_user_model()
                    user = User.objects.filter(email=pending_email).first()

                    # user = authenticate(request, username=pending_email)
                    print(f"🔐 Autenticando a {pending_email}")
                    print(f"🔐 Usuario autenticado: {user}")
                    
                    if user:
                        login(request, user)  # Inicia sesión sin re-autenticar
                        del security_codes[pending_email]  # Elimina código usado
                        request.session.pop("pending_email", None)  # Limpia la sesión
                        return redirect("base")  # Redirige a base
                    else:
                        error = "Hubo un problema con la autenticación."

                
                else:
                    error = "Código incorrecto. Intenta nuevamente."
            except ValueError:
                error = "Código inválido. Debe ser un número."
        else:
            error = "Código no válido o expirado."

        return render(request, "core/verify_code.html", {"error": error})

    return render(request, "core/verify_code.html")



def send_verification_email(user_email, user_name, code):
    subject = "Código de Verificación"
    
    # Cargar el template con los valores
    html_content = render_to_string("core/email_verification.html", {
        "user_name": user_name,
        "verification_code": code
    })
    
    text_content = strip_tags(html_content)  # Extrae solo el texto sin HTML
    
    email = EmailMultiAlternatives(
        subject,
        text_content,
        "leanvarela6@gmail.com",  # Remitente
        [user_email]  # Destinatario
    )
    
    email.attach_alternative(html_content, "text/html")  # Adjunta la versión HTML
    email.send()



@login_required
@never_cache
def base_view(request):
    """ Carga base.html con contenido dinámico """
    response = render(request, "core/base.html",{
        'user_mail': request.user.email
    })
    response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    return response

@login_required
def forwarding_pdf_view(request):
    """ Carga la vista de creación de cotizaciones dentro de base.html """
    return render(request, "core/base.html", {"content_template": "forwardingCR/Form_forwardingCR_PDF.html"})

def logout_view(request):
    """ Cerrar sesión y redirigir al login """
    logout(request)
    return redirect("login")