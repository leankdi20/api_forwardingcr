from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

def trigger_error(request):
    division_by_zero = 1 / 0  # Provoca un error para probar Sentry


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("base/", views.base_view, name="base"),  
    path('forwardingCR/create/', views.forwarding_pdf_view, name='createPdfFCR'), 
    path("verify-code/", views.verify_code_view, name="verify_code"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)