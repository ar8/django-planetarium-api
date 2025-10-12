from django.db import models


# Create your models here.
class Terrain(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Terrain'
        verbose_name_plural = 'Terrains'
        db_table = 'terrains'


class Climate(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Climate'
        verbose_name_plural = 'Climates'
        db_table = 'climates'


class Planet(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    population = models.BigIntegerField(null=True, blank=True)
    terrains = models.ManyToManyField(Terrain, related_name='planets', blank=True)
    climates = models.ManyToManyField(Climate, related_name='planets', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Planet'
        verbose_name_plural = 'Planets'
        db_table = 'planets'
