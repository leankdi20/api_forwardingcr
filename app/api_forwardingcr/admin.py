from django.contrib import admin
from .models import Cotizacion, DetailDelivery, ServiceInformation, chargeService
# Register your models here.


admin.site.register(Cotizacion)
admin.site.register(DetailDelivery)
admin.site.register(ServiceInformation)
admin.site.register(chargeService)