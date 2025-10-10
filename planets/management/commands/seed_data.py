from django.core.management.base import BaseCommand
from planets.models import Planet, Terrain, Climate


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Flush database first
        self.flush_data()

        # Create terrains
        terrain1 = Terrain.objects.create(name='Rocky')
        terrain2 = Terrain.objects.create(name='Ocean')
        terrain3 = Terrain.objects.create(name='Desert')
        Terrain.objects.create(name='Grasslands')
        Terrain.objects.create(name='Mountains')
        Terrain.objects.create(name='Plains')
        Terrain.objects.create(name='Lakes')
        Terrain.objects.create(name='Islands')

        # Create climates
        climate1 = Climate.objects.create(name='Tropical')
        climate2 = Climate.objects.create(name='Arid')
        climate3 = Climate.objects.create(name='Temperate')
        Climate.objects.create(name='Mild')
        Climate.objects.create(name='Humid')

        # Create planets
        p1 = Planet.objects.create(
            name='Earth',
            population=7800000000
        )
        p1.terrains.set([terrain1, terrain2])
        p1.climates.set([climate1, climate3])
    
        p2 = Planet.objects.create(
            name='Mars',
            population=0
        )
        p2.terrains.set([terrain1])
        p2.climates.set([climate2])

        p3 = Planet.objects.create(
            name='Venus',
            population=0
        )
        p3.terrains.set([terrain3])
        p3.climates.set([climate1])

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def flush_data(self):
        Planet.objects.all().delete()
        Terrain.objects.all().delete()
        Climate.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Database flushed successfully!'))