from django.shortcuts import render

# service view
from django.http import JsonResponse
from django.views import View
from .services import fetch_planets_service
from .models import Planet, Terrain, Climate
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
                if planet.get('terrains'):
                    terrain_objects = []
                    for terrain_name in planet['terrains']:

                        terrain, _ = Terrain.objects.get_or_create(name=terrain_name)
                        terrain_objects.append(terrain)
                    planet_obj.terrains.set(terrain_objects)
                if planet.get('climates'):
                    climate_objects = []
                    for climate_name in planet['climates']:
                        # important: to avoid duplicates, get or create climate
                        climate, _ = Climate.objects.get_or_create(name=climate_name)
                        climate_objects.append(climate)
                    planet_obj.climates.set(climate_objects)

        # Fetch all planet objects from the database, to double check adding new ones
        data = Planet.objects.all().values()

        return JsonResponse({
            'status': 'success',
            'total_planets': len(data),
            'planets': list(data)
        }, safe=False)
