from django.db import models


# Create your models here.
class Cotizacion(models.Model):
    quotation_number = models.CharField(max_length=50, unique=True)
    date_time = models.DateField()
    expiration_date = models.DateField()
    contact_person = models.EmailField(max_length=100)
    estado_cotizacion = models.BooleanField(default=True)
    subtotal_cotizacion = models.DecimalField(max_digits=10, decimal_places=2)
    iva_13 = models.DecimalField(max_digits=10, decimal_places=2)
    total_cotizacion = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField()

class DetailDelivery(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalle_envio')
    contact_details = models.TextField()
    delivery_address = models.TextField()
    type_of_movement = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)


class ServiceInformation(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='informacion_servicio')
    package = models.IntegerField()
    description = models.CharField(max_length=200)
    gross_weight = models.DecimalField(max_digits=10, decimal_places=2)
    type_volume = models.CharField(max_length=50)
    metroCubicoVolumen = models.CharField(max_length=50)
    resultado_volume = models.DecimalField(max_digits=10, decimal_places=2)
    volume_weight = models.DecimalField(max_digits=10, decimal_places=2)
    iva_boolean = models.BooleanField(default=False)
    price_service = models.DecimalField(max_digits=10, decimal_places=2)
    amount_service = models.DecimalField(max_digits=10, decimal_places=2)

class chargeService(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='cargo_servicio')
    description_of_charges = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price_charge = models.DecimalField(max_digits=10, decimal_places=2)
    amount_charge = models.DecimalField(max_digits=10, decimal_places=2)





