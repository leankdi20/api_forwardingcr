from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cotizaciones', views.CotizacionViewSet)
router.register(r'ver-cotizaciones', views.CotizacionVer)
router.register(r'detalles', views.DetailDeliveryViewSet)
router.register(r'servicios', views.ServiceInformationViewSet)
router.register(r'cargos', views.ChargeServiceViewSet)

app_name = 'api_forwardingcr'
urlpatterns = [
    path('', include(router.urls)),
]