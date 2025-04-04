from rest_framework import serializers
from .models import Cotizacion, DetailDelivery, ServiceInformation, chargeService

class DetailDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailDelivery
        
        exclude = ['cotizacion']

class ServiceInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceInformation
        
        exclude = ['cotizacion']

class ChargeServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = chargeService
    
        exclude = ['cotizacion']


# Solo para leer todas
class CotizacionReadSerializer(serializers.ModelSerializer):
    detalle_envio = DetailDeliverySerializer(many=True, required=False)
    informacion_servicio = ServiceInformationSerializer(many=True, required=False)
    cargo_servicio = ChargeServiceSerializer(many=True, required=False)

    class Meta:
        model = Cotizacion
        fields = '__all__'


class CotizacionSerializer(serializers.ModelSerializer):
    detalle_envio = DetailDeliverySerializer(many=True)
    informacion_servicio = ServiceInformationSerializer(many=True)
    cargo_servicio = ChargeServiceSerializer(many=True)

    class Meta:
        model = Cotizacion
        fields = '__all__'

    def create(self, validated_data):
        detalle_data = validated_data.pop('detalle_envio', [])
        info_data = validated_data.pop('informacion_servicio', [])
        cargo_data = validated_data.pop('cargo_servicio', [])

        cotizacion = Cotizacion.objects.create(**validated_data)

        for detalle in detalle_data:
            DetailDelivery.objects.create(cotizacion=cotizacion, **detalle)
        for info in info_data:
            ServiceInformation.objects.create(cotizacion=cotizacion, **info)
        for cargo in cargo_data:
            chargeService.objects.create(cotizacion=cotizacion, **cargo)

        return cotizacion
