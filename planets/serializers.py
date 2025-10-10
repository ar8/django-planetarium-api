from rest_framework import serializers
from .models import Planet, Terrain, Climate
from django.db import models

# token authentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class PlanetSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    population = serializers.IntegerField()
    terrains = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Terrain.objects.all()
    )
    climates = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Climate.objects.all()
    )
    id = serializers.ReadOnlyField()

    class Meta:
        model = Planet
        fields = ['id', 'name', 'population', 'terrains', 'climates', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        ordering = ['name']
        verbose_name = 'Planet'
        verbose_name_plural = 'Planets'
        db_table = 'planet'
        indexes = [
            models.Index(fields=['name'], name='planet_name_idx'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_planet_name')
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        return token
