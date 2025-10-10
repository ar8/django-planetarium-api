from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from .services import fetch_planets_service
from .models import Planet


class PlanetServiceView(View):
    def get(self, request):
        planets = fetch_planets_service()
        planet_list = []

        for planet in planets:
            planet_object = Planet(
                name=planet['name'],
                population=planet['population'],
                terrains=planet['terrains'],
                climates=planet['climates']
            )
            planet_list.append(planet_object)

        Planet.objects.bulk_create(planet_list, ignore_conflicts=True, batch_size=10)
        # Fetch all planet objects from the database
        data = Planet.objects.all().values()

        return JsonResponse({
            'status': 'success',
            'total_planets': len(data),
            'planets': list(data)
        }, safe=False)