from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from .models import Planet
from .serializers import PlanetSerializer
from django.http import Http404
from rest_framework import serializers

# pagination
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

# token authentication and security
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

# cache
from django.core.cache import cache


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    helper functions to get Bearer token to test security of the API
    Example: http://localhost:8000/auth/token/
    """
    serializer_class = CustomTokenObtainPairSerializer


# -----------------------------
# Planet API
# -----------------------------
class PlanetPagination(LimitOffsetPagination, PageNumberPagination):
    """
    example:
    planets/?page=2 => get page 2
    planets/?page=3&page_size=5 => page 3, with 5 results per page
    planets/?limit=5&offset=10 => skip 10, return 5
    """
    default_limit = 10
    page_size_query_param = 'page_size'
    max_limit = 100
    page_size = 10
    page_query_param = 'page'
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_page_size = 100


class PlanetListAPIView(ListAPIView):
    """
    Get all planets, filter, search, order, paginate
    example:
    planets/
    planets/?name=Earth
    planets/?climates=temperate
    planets/?terrains=forest
    planets/?population=1000
    planets/?search=Earth
    planets/?ordering=name
    planets/?ordering=-population
    planets/?page=2
    planets/?page=3&page_size=5
    planets/?limit=5&offset=10
    planets/?climates__name=temperate
    planets/?terrains__name=forest
    planets/?population__gte=1000&population__lte=5000
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    # security - only authenticated users
    # permission_classes = [IsAuthenticated] # TODO: commented for testing
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    pagination_class = PlanetPagination
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'climates__name': ['exact', 'icontains'],
        'terrains__name': ['exact', 'icontains'],
        'population': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte'],
        'updated_at': ['exact', 'gte', 'lte'],
    }
    search_fields = ('name', 'climates__name', 'terrains__name', 'population', 'created_at', 'updated_at')
    ordering_fields = ('name', 'created_at', 'updated_at')
    ordering = ('name',)  # default ordering

    # override get_queryset to customize queryset if needed
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class PlanetDetailAPIView(RetrieveAPIView):
    """
    Get a planet by name
    example:
    planets/name/Earth/
    planets/name/Mars/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    # security - only authenticated users
    # permission_classes = [IsAuthenticated] # TODO: commented for testing
    # lookup by name instead of id
    lookup_field = 'name'

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise Http404("Planet not found")


class PlanetCreateAPIView(CreateAPIView):
    """
    Create a new planet
    /api/v1/planets/create/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    # security - only authenticated users
    # permission_classes = [IsAuthenticated] # TODO: commented for testing

    def perform_create(self, serializer):
        planet_name = serializer.validated_data.get('name')
        if Planet.objects.filter(name=planet_name).exists():
            raise serializers.ValidationError("Planet with this name already exists.")
        serializer.save()
        # Cache
        planet = Planet.objects.get(name=planet_name)
        cache_key = f'planet_data_{planet.id}'
        cache.set(cache_key, serializer.data, timeout=60 * 15)


class PlanetUpdateAPIView(RetrieveUpdateAPIView):
    """
    Update a planet by name
    /api/v1/planets/update/Earth/
    /api/v1/planets/update/Mars/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    # security - only authenticated users
    permission_classes = [IsAuthenticated]
    # lookup by name instead of id
    lookup_field = 'name'

    def perform_update(self, serializer):
        planet_name = serializer.validated_data.get('name')
        if Planet.objects.filter(name=planet_name).exists():
            raise serializers.ValidationError("Planet with this name already exists.")
        serializer.save()
        # Cache
        planet = Planet.objects.get(name=planet_name)
        cache_key = f'planet_data_{planet.id}'
        cache.set(cache_key, serializer.data, timeout=60 * 15)


class PlanetDeleteAPIView(DestroyAPIView):
    """
    Delete a planet by name
    /api/v1/planets/delete/Earth/
    /api/v1/planets/delete/Mars/
    """
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    # security - only authenticated users
    permission_classes = [IsAuthenticated]
    # lookup by name instead of id
    lookup_field = 'name'

    def delete(self, request, *args, **kwargs):
        # delete the cache
        cache.delete('planet_data_{}'.format(kwargs['name']))
        return super().delete(request, *args, **kwargs)
