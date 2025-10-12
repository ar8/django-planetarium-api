from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views import View
from .services import fetch_planets_service
from .models import Planet
from django.db import transaction


class PlanetServiceView(View):
    def get(self, request):
        planets_data = fetch_planets_service()

        for planet in planets_data:
            # Use transaction to avoid partial saves
            with transaction.atomic():
                planet_obj, created = Planet.objects.get_or_create(
                    name=planet['name'],
                    defaults={'population': planet['population']}
                )
                if planet['terrains']:
                    planet_obj.terrains.set(planet['terrains'])
                if planet['climates']:
                    planet_obj.climates.set(planet['climates'])

        # Fetch all planet objects from the database
        data = Planet.objects.all().values()

        return JsonResponse({
            'status': 'success',
            'total_planets': len(data),
            'planets': list(data)
        }, safe=False)