from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins,views
from .models import Cotizacion, DetailDelivery, ServiceInformation, chargeService
from .serializers import CotizacionSerializer, DetailDeliverySerializer, ServiceInformationSerializer, ChargeServiceSerializer, CotizacionReadSerializer

class CotizacionViewSet(viewsets.ModelViewSet):
    queryset = Cotizacion.objects.all()
    serializer_class = CotizacionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        quotation_number = self.request.GET.get("quotation_number")
        contact_person = self.request.GET.get("contact_person")

        if quotation_number:
            queryset = queryset.filter(quotation_number__icontains=quotation_number)
        if contact_person:
            queryset = queryset.filter(contact_person__icontains=contact_person)

        return queryset
    

class CotizacionVer(mixins.RetrieveModelMixin,mixins.ListModelMixin,viewsets.GenericViewSet):
    queryset= Cotizacion.objects.all()
    serializer_class = CotizacionReadSerializer

    def get_queryset(self):

        query = self.queryset

        quotation_number = self.request.GET.get("quotation_number")
        contact_person = self.request.GET.get("contact_person")

        if(quotation_number):
            query = query.filter(quotation_number__icontains= quotation_number)

        if (contact_person):
            query = query.filter(contact_person__icontains = contact_person)
    

        return query.all()

class DetailDeliveryViewSet(viewsets.ModelViewSet):
    queryset = DetailDelivery.objects.all()
    serializer_class = DetailDeliverySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        type_of_movement = self.request.GET.get("type_of_movement")
        origin = self.request.GET.get("origin")
        destination = self.request.GET.get("destination")

        if type_of_movement:
            queryset = queryset.filter(type_of_movement__icontains=type_of_movement)
        if origin:
            queryset = queryset.filter(origin__icontains=origin)
        if destination:
            queryset = queryset.filter(destination__icontains=destination)
        return queryset



class ServiceInformationViewSet(viewsets.ModelViewSet):
    queryset = ServiceInformation.objects.all()
    serializer_class = ServiceInformationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        description = self.request.GET.get("description")
        type_volume = self.request.GET.get("type_volume")

        if description:
            queryset = queryset.filter(description__icontains=description)
        if type_volume:
            queryset = queryset.filter(type_volume__icontains=type_volume)
        return queryset



class ChargeServiceViewSet(viewsets.ModelViewSet):
    queryset = chargeService.objects.all()
    serializer_class = ChargeServiceSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        description_of_charges = self.request.GET.get("description_of_charges")
        if description_of_charges:
            queryset = queryset.filter(description_of_charges__icontains=description_of_charges)
        return queryset