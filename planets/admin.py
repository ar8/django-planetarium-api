from django.contrib import admin
from . import models


@admin.register(models.Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = ('name', 'population', 'get_terrains', 'get_climates', 'created_at', 'updated_at')
    search_fields = ('name', 'terrains__name', 'climates__name')
    list_filter = ('climates__name', 'terrains__name', 'created_at', 'updated_at')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    def created_at_with_seconds(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
    created_at_with_seconds.short_description = 'Created At'

    def updated_at_with_seconds(self, obj):
        return obj.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    updated_at_with_seconds.short_description = 'Updated At'

    def get_terrains(self, obj):
        return ", ".join([terrain.name for terrain in obj.terrains.all()])
    get_terrains.short_description = 'Terrains'

    def get_climates(self, obj):
        return ", ".join([climate.name for climate in obj.climates.all()])
    get_climates.short_description = 'Climates'


@admin.register(models.Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(models.Climate)
class ClimateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
