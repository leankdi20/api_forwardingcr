import requests
import json
from pathlib import Path
from .models import Cotizacion, DetailDelivery, ServiceInformation, chargeService

def crear_cotizacion_de_prueba():
    url = "http://localhost:8000/api/cotizaciones/"
    
    data = {
        "quotation_number": "FCR-00126",
        "date_time": "2025-04-02",
        "expiration_date": "2025-04-15",
        "contact_person": "Carlos Rojas",
        "estado_cotizacion": True,
        "subtotal_cotizacion": 2500.00,
        "iva_13": 325.00,
        "total_cotizacion": 2825.00,
        "notes": "Cotización con múltiples cargos",

        "detalle_envio": [
            {
            "contact_details": "Oficina Central, +506 8888 0000",
            "delivery_address": "San José, Costa Rica",
            "type_of_movement": "Aéreo",
            "origin": "Miami",
            "destination": "San José"
            }
        ],

        "informacion_servicio": [
            {
            "package": 1,
            "description": "Material promocional",
            "gross_weight": 50.0,
            "type_volume": "Cúbico",
            "metroCubicoVolumen": '100x50x50',
            "resultado_volume": 200.0,
            "volume_weight": 180.0,
            "iva_boolean": True,
            "price_service": 1500.00,
            "amount_service": 1500.00
            }
        ],

        "cargo_servicio": [
            {
            "description_of_charges": "Seguro internacional",
            "quantity": 1,
            "price_charge": 300.00,
            "amount_charge": 300.00
            },
            {
            "description_of_charges": "Manejo en aduana",
            "quantity": 1,
            "price_charge": 700.00,
            "amount_charge": 700.00
            }
        ]
        }


    response = requests.post(url, json=data)

    print(f"Status code: {response.status_code}")
    try:
        print(response.json())
    except Exception as e:
        print("Error al parsear JSON:")
        print(response.text)


def cargar_json_directamente():
    ruta_json = Path(__file__).resolve().parent / "media" / "cotizaciones_prueba.json"

    with open(ruta_json, encoding='utf-8') as file:
        cotizaciones = json.load(file)

    
    for data in cotizaciones:
        cotizacion, _ = Cotizacion.objects.update_or_create(
            quotation_number=data["quotation_number"],
            defaults={
                "date_time": data["date_time"],
                "expiration_date": data["expiration_date"],
                "contact_person": data["contact_person"],
                "estado_cotizacion": data["estado_cotizacion"],
                "subtotal_cotizacion": data["subtotal_cotizacion"],
                "iva_13": data["iva_13"],
                "total_cotizacion": data["total_cotizacion"],
                "notes": data["notes"],
            }
        )

        # Limpiamos relaciones existentes (opcional si querés evitar duplicados)
        cotizacion.detalle_envio.all().delete()
        cotizacion.informacion_servicio.all().delete()
        cotizacion.cargo_servicio.all().delete()

        for d in data.get("detalle_envio", []):
            DetailDelivery.objects.create(cotizacion=cotizacion, **d)

        for s in data.get("informacion_servicio", []):
            ServiceInformation.objects.create(cotizacion=cotizacion, **s)

        for c in data.get("cargo_servicio", []):
            chargeService.objects.create(cotizacion=cotizacion, **c)

    print("¡Carga completada con update_or_create!")
    